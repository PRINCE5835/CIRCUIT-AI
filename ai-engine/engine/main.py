import logging
import json
import base64
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager

from .core.config import settings
from .core.model_registry import registry
from .llm.ollama_client import client as ollama_client
from .llm.prompts.circuit_generation import CIRCUIT_GENERATION_SYSTEM
from .llm.prompts.repair_diagnosis import REPAIR_DIAGNOSIS_SYSTEM
from .llm.prompts.learning_tutor import LEARNING_TUTOR_SYSTEM
from .llm.prompts.component_info import COMPONENT_INFO_SYSTEM
from .speech.stt.vosk_handler import handler as vosk_handler
from .speech.stt.whisper_handler import handler as whisper_handler
from .classifier import classify, QueryType
from .content import sources as content_sources

logger = logging.getLogger(__name__)

SYSTEM_PROMPTS: dict[QueryType, str] = {
    "circuit_generation": CIRCUIT_GENERATION_SYSTEM,
    "repair": REPAIR_DIAGNOSIS_SYSTEM,
    "verification": COMPONENT_INFO_SYSTEM,
    "learning": LEARNING_TUTOR_SYSTEM,
    "marketplace": (
        "You are an electronics component marketplace assistant. "
        "Help users find components, compare prices, and suggest suitable parts "
        "for their projects. Provide source URLs when available."
    ),
    "general": (
        "You are BreadBoard AI, an expert electronics engineering assistant. "
        "You help users with circuit design, component selection, troubleshooting, "
        "and learning electronics. "
        "Be conversational and friendly — greet users warmly, ask clarifying questions, "
        "and provide detailed step-by-step guidance. "
        "If the user says 'hi', 'hello', 'hey', or greets you, respond with a warm "
        "greeting introducing yourself and asking how you can help with electronics. "
        "Answer from your knowledge with specificity. "
        "If asked about a specific circuit, provide wiring steps, component lists, "
        "and explanations. Always include source URLs and datasheet references."
    ),
}


def _last_user_message(messages: list[dict]) -> str:
    for m in reversed(messages):
        if m.get("role") == "user":
            return m.get("content", "")
    return ""


def _collect_source_urls(messages: list[dict]) -> list[dict]:
    urls = []
    for m in messages:
        if m.get("role") == "system" and "sources" in m:
            urls.extend(m.get("sources", []))
    return urls


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("BreadBoard AI Engine starting — environment: %s", settings.environment)
    await vosk_handler.load()
    try:
        await whisper_handler.load()
    except Exception:
        logger.warning("Whisper not available (install openai-whisper)")
    yield
    await ollama_client.close()
    logger.info("AI Engine shut down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/health")
async def health(request: Request):
    try:
        models = await ollama_client.list_models()
        ollama_ok = len(models) > 0
    except Exception:
        ollama_ok = False
    return {
        "status": "healthy",
        "ollama": ollama_ok,
        "models_available": len(registry.list_available()),
        "whisper_loaded": whisper_handler._available,
        "vosk_loaded": vosk_handler._available,
        "piper_available": False,
    }


@app.get("/api/v1/models")
async def list_models():
    return {
        "available": [{
            "name": m.name,
            "provider": m.provider.value,
            "capabilities": [c.value for c in m.capability],
            "downloaded": m.is_downloaded,
        } for m in registry.list_available()],
        "all": [{
            "name": m.name,
            "provider": m.provider.value,
            "capabilities": [c.value for c in m.capability],
            "size_mb": m.size_mb,
            "downloaded": m.is_downloaded,
        } for m in registry._models.values()],
    }


@app.get("/api/v1/models/primary")
async def primary_model():
    m = registry.get_primary()
    return {"name": m.name, "provider": m.provider.value, "ollama_tag": m.ollama_tag}


@app.post("/api/v1/chat")
async def chat(body: dict):
    messages = body.get("messages", [])
    model = body.get("model", settings.ollama_primary_model)
    temperature = body.get("temperature", 0.7)
    max_tokens = body.get("max_tokens", 512)
    stream = body.get("stream", False)

    if not messages:
        raise HTTPException(status_code=400, detail="Messages are required")

    query = _last_user_message(messages)
    query_type = classify(query)

    matched_circuits = content_sources.search_circuits(query)
    source_urls = []

    system_prompt = SYSTEM_PROMPTS.get(query_type, SYSTEM_PROMPTS["general"])

    if matched_circuits:
        circuit_titles = ", ".join(c["title"] for c in matched_circuits[:5])
        system_prompt += f"\n\nKnown circuits: {circuit_titles}."
        for c in matched_circuits[:3]:
            for src in c["sources"]:
                source_urls.append({"title": src["name"], "url": src["url"]})

    messages = [{"role": "system", "content": system_prompt}] + messages

    async def _stream():
        yield f"data: {json.dumps({'type': 'meta', 'query_type': query_type, 'model': model, 'sources': source_urls, 'matched_circuits': [c['title'] for c in matched_circuits]})}\n\n"
        full_content = ""
        try:
            async for chunk in ollama_client.chat(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            ):
                content = chunk.get("message", {}).get("content", "")
                if content:
                    full_content += content
                    yield f"data: {json.dumps({'type': 'token', 'token': content})}\n\n"
                if chunk.get("done"):
                    yield f"data: {json.dumps({'type': 'done', 'content': full_content})}\n\n"
        except Exception as e:
            logger.error("Streaming error: %s", str(e))
            yield f"data: {json.dumps({'type': 'error', 'detail': str(e)})}\n\n"

    if stream:
        return StreamingResponse(_stream(), media_type="text/event-stream")

    result = []
    async for chunk in ollama_client.chat(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    ):
        result.append(chunk)
    response = result[0] if result else {}
    content = response.get("message", {}).get("content", "")
    return {
        "response": content,
        "model": model,
        "query_type": query_type,
        "sources": source_urls,
        "matched_circuits": [c["title"] for c in matched_circuits],
    }


@app.post("/api/v1/generate")
async def generate(body: dict):
    prompt = body.get("prompt", "")
    model = body.get("model", settings.ollama_primary_model)
    temperature = body.get("temperature", 0.2)
    max_tokens = body.get("max_tokens", 4096)

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    try:
        response = await ollama_client.generate(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return {"response": response, "model": model}
    except Exception as e:
        logger.error("Generate error: %s", str(e))
        raise HTTPException(status_code=502, detail=f"AI Engine error: {str(e)}")


@app.post("/api/v1/circuit/generate")
async def generate_circuit(body: dict):
    description = body.get("description", "")
    model = body.get("model", settings.ollama_primary_model)
    temperature = body.get("temperature", 0.3)
    max_tokens = body.get("max_tokens", 4096)

    if not description:
        raise HTTPException(status_code=400, detail="Description is required")

    matched = content_sources.search_circuits(description)
    system_prompt = CIRCUIT_GENERATION_SYSTEM
    if matched:
        titles = ", ".join(c["title"] for c in matched[:5])
        system_prompt += f" Known circuits: {titles}."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": description},
    ]

    try:
        response = await ollama_client.chat_sync(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return {
            "response": response,
            "model": model,
            "sources": [s for c in matched for s in c["sources"]],
        }
    except Exception as e:
        logger.error("Circuit generation error: %s", str(e))
        raise HTTPException(status_code=502, detail=f"AI Engine error: {str(e)}")


@app.post("/api/v1/speech/stt")
async def transcribe(body: dict):
    audio_b64 = body.get("audio", "")

    if not audio_b64:
        raise HTTPException(status_code=400, detail="Audio data is required")

    try:
        wav_bytes = base64.b64decode(audio_b64)
        result = await vosk_handler.transcribe_bytes(wav_bytes)
        return result
    except Exception as e:
        logger.error("STT error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"STT error: {str(e)}")


@app.post("/api/v1/speech/tts")
async def synthesize(body: dict):
    return {"message": "TTS not configured yet"}


@app.post("/api/v1/vision/detect")
async def detect_components(body: dict):
    image_b64 = body.get("image", "")
    if not image_b64:
        raise HTTPException(status_code=400, detail="Image data is required")

    try:
        import json as _json

        prompt = (
            "You are an expert electronics component analyzer. Carefully examine the provided image.\n\n"
            "RULES:\n"
            "- If NO circuit board, electronic components, or electronic parts are visible, return: "
            "{\"status\": \"no_circuit\", \"message\": \"No electronic circuit or components detected in the image.\"}\n"
            "- If the image is blurry, unclear, or too dark to identify components clearly, return: "
            "{\"status\": \"unclear\", \"message\": \"The image is not clear enough. Please capture a clearer photo with good lighting.\"}\n"
            "- If components ARE visible, perform a DEEP SCAN and identify every component with as much detail as possible.\n\n"
            "For each detected component, provide:\n"
            "  - name: exact component name/type (e.g., \"Resistor 220Ω\", \"LM358 Op-Amp\", \"10µF 16V Capacitor\")\n"
            "  - type: component category (resistor, capacitor, IC, transistor, diode, LED, connector, etc.)\n"
            "  - confidence: 0.0 to 1.0\n"
            "  - quantity: number of identical components found\n"
            "  - package: package type if visible (e.g., \"SMD-0805\", \"DIP-8\", \"TO-220\", \"0603\", \"THT\")\n"
            "  - markings: any text/labels visible on the component\n\n"
            "Return ONLY valid JSON. No markdown, no explanations outside the JSON.\n\n"
            "SUCCESS FORMAT:\n"
            "{\"status\": \"success\", \"components\": [{\"name\": \"...\", \"type\": \"...\", \"confidence\": 0.95, \"quantity\": 2, \"package\": \"...\", \"markings\": \"...\"}, ...]}\n\n"
            "NO_CIRCUIT FORMAT:\n"
            "{\"status\": \"no_circuit\", \"message\": \"...\"}\n\n"
            "UNCLEAR FORMAT:\n"
            "{\"status\": \"unclear\", \"message\": \"...\"}"
        )

        # Send image to LLaVA via Ollama's /api/generate with images array
        payload = {
            "model": "llava",
            "prompt": prompt,
            "images": [image_b64],
            "options": {
                "temperature": 0.1,
                "num_predict": 4096,
            },
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post("http://localhost:11434/api/generate", json=payload)
            resp.raise_for_status()
            data = resp.json()
            raw = data.get("response", "")

        raw = raw.replace("```json", "").replace("```", "").strip()
        result = _json.loads(raw)

        status = result.get("status", "success")
        if status == "no_circuit":
            return {"status": "no_circuit", "message": result.get("message", "No electronic circuit or components detected."), "model": "llava"}
        if status == "unclear":
            return {"status": "unclear", "message": result.get("message", "Image is not clear enough."), "model": "llava"}

        components = result.get("components", [])
        if isinstance(components, list) and components:
            return {"status": "success", "components": components, "model": "llava"}
        else:
            return {"status": "no_circuit", "message": "No electronic components could be identified in the image.", "model": "llava"}

    except Exception as e:
        logger.error("Vision detection error: %s", str(e))

    return {"status": "error", "message": "Vision detection failed. Please try again with a clearer image.", "components": []}


@app.post("/api/v1/cost/estimate")
async def estimate_cost(body: dict):
    components = body.get("components", [])
    if not components:
        raise HTTPException(status_code=400, detail="Components list is required")

    try:
        prompt = (
            f"Estimate the cost of these electronic components in INR: {components}. "
            "Return a JSON object with 'total_cost', 'currency': 'INR', "
            "and 'breakdown' as a list of {name, quantity, unit_price, total}. "
            "Only return the JSON."
        )
        response = await ollama_client.generate(
            model=settings.ollama_light_model,
            prompt=prompt,
            temperature=0.1,
            max_tokens=2048,
        )
        raw = response.strip() if isinstance(response, str) else response.get("response", "")
        import json as _json
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = _json.loads(raw)
        return {**result, "model": settings.ollama_light_model}
    except Exception as e:
        logger.error("Cost estimation error: %s", str(e))
        return {"message": "Cost estimation not configured yet"}
