import logging
import base64
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .core.model_registry import registry
from .llm.ollama_client import client as ollama_client
from .llm.prompts.circuit_generation import CIRCUIT_GENERATION_SYSTEM
from .llm.prompts.repair_diagnosis import REPAIR_DIAGNOSIS_SYSTEM
from .llm.prompts.learning_tutor import LEARNING_TUTOR_SYSTEM
from .llm.prompts.component_info import COMPONENT_INFO_SYSTEM
from .speech.stt.vosk_handler import handler as vosk_handler
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
        "and learning electronics. Answer from your knowledge with specificity. "
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
        "whisper_loaded": False,
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

    try:
        result = []
        async for chunk in ollama_client.chat(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        ):
            result.append(chunk)
        if stream:
            return result
        response = result[0] if result else {}
        content = response.get("message", {}).get("content", "")
        return {
            "response": content,
            "model": model,
            "query_type": query_type,
            "sources": source_urls,
            "matched_circuits": [c["title"] for c in matched_circuits],
        }
    except Exception as e:
        logger.error("Chat error: %s", str(e))
        raise HTTPException(status_code=502, detail=f"AI Engine error: {str(e)}")


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
    return {"message": "Vision detection not configured yet"}


@app.post("/api/v1/cost/estimate")
async def estimate_cost(body: dict):
    return {"message": "Cost estimation not configured yet"}
