from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.services.ai_service import ai_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/health")
async def ai_health():
    try:
        return await ai_service.health()
    except Exception:
        return await ai_service.ollama_health()


@router.get("/models")
async def list_models():
    try:
        return await ai_service.list_models()
    except Exception:
        return {"current_model": settings.ollama_model, "status": "direct"}


@router.get("/models/primary")
async def primary_model():
    try:
        return await ai_service.get_primary_model()
    except Exception:
        return {"model": settings.ollama_model, "status": "direct"}


@router.post("/chat")
async def chat(body: dict, current_user: User = Depends(get_current_user)):
    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="Messages are required")

    model = body.get("model")
    try:
        result = await ai_service.chat(
            messages=messages,
            model=model,
        )
        response = result.get("message", {}).get("content", "") or result.get("response", "")
        sources = result.get("sources", [])
        query_type = result.get("query_type", "general")
        matched_circuits = result.get("matched_circuits", [])
        return {
            "response": response,
            "model": model or settings.ollama_model,
            "query_type": query_type,
            "sources": sources,
            "matched_circuits": matched_circuits,
        }
    except Exception:
        prompt = "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages])
        result = await ai_service.ollama_generate(
            prompt=prompt,
            model=model,
        )
        return {
            "response": result.get("response", ""),
            "model": result.get("model", settings.ollama_model),
        }


@router.post("/generate")
async def generate(body: dict, current_user: User = Depends(get_current_user)):
    prompt = body.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    model = body.get("model")
    try:
        result = await ai_service.generate(prompt=prompt, model=model)
        return {"response": result.get("response", ""), "model": model or settings.ollama_model}
    except Exception:
        result = await ai_service.ollama_generate(prompt=prompt, model=model)
        return {
            "response": result.get("response", ""),
            "model": result.get("model", settings.ollama_model),
        }


@router.post("/circuit/generate")
async def generate_circuit(body: dict, current_user: User = Depends(get_current_user)):
    description = body.get("description", "")
    if not description:
        raise HTTPException(status_code=400, detail="Description is required")

    try:
        result = await ai_service.generate_circuit(description=description)
        response = result.get("response", "")
        sources = result.get("sources", [])
        return {
            "response": response,
            "sources": sources,
        }
    except Exception:
        prompt = (
            "Generate an electronics circuit.\n\n"
            f"Description:\n{description}\n\n"
            "Return:\n1. Components list\n2. Connections\n3. Explanation"
        )
        return await ai_service.ollama_generate(prompt=prompt)


@router.post("/speech/stt")
async def transcribe(body: dict, current_user: User = Depends(get_current_user)):
    try:
        return await ai_service.transcribe(
            audio_base64=body.get("audio", ""),
            language=body.get("language", "en"),
        )
    except Exception:
        return {"message": "STT not configured yet"}


@router.post("/speech/tts")
async def synthesize(body: dict, current_user: User = Depends(get_current_user)):
    try:
        return await ai_service.synthesize(
            text=body.get("text", ""),
            voice=body.get("voice", "default"),
        )
    except Exception:
        return {"message": "TTS not configured yet"}


@router.post("/vision/detect")
async def detect_components(body: dict, current_user: User = Depends(get_current_user)):
    try:
        return await ai_service.detect_components(
            image_base64=body.get("image", ""),
        )
    except Exception:
        return {"message": "Vision detection not configured yet"}


@router.post("/cost/estimate")
async def estimate_cost(body: dict, current_user: User = Depends(get_current_user)):
    try:
        return await ai_service.estimate_cost(
            components=body.get("components", []),
        )
    except Exception:
        return {"message": "Cost estimation not configured yet"}
