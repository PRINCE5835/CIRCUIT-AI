import logging
import re

from fastapi import APIRouter, Depends

logger = logging.getLogger(__name__)
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.services.ai_service import ai_service
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.db.repository import BaseRepository
from app.schemas.ai import (
    ChatRequest,
    ChatStreamRequest,
    GenerateRequest,
    CircuitGenerateRequest,
    STTRequest,
    TTSRequest,
    VisionDetectRequest,
    CostEstimateRequest,
)

router = APIRouter()


def _detect_language(text: str) -> str:
    if not text:
        return "en"
    hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
    bengali_chars = len(re.findall(r'[\u0980-\u09FF]', text))
    if hindi_chars > 3 or bengali_chars > 3:
        return "hi" if hindi_chars >= bengali_chars else "bn"
    return "en"


def _language_instruction(text: str) -> str:
    lang = _detect_language(text)
    if lang == "hi":
        return "IMPORTANT: Respond in Hindi (हिंदी). Use the same language as the user's message."
    return "IMPORTANT: Respond in the same language as the user's message."


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
async def chat(
    body: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    messages = body.messages
    model = body.model
    conversation_id = body.conversation_id
    repo = BaseRepository(Conversation, db)

    try:
        result = await ai_service.chat(
            messages=messages,
            model=model,
        )
        response = result.get("message", {}).get("content", "") or result.get("response", "")
        sources = result.get("sources", [])
        query_type = result.get("query_type", "general")
        matched_circuits = result.get("matched_circuits", [])
    except Exception:
        user_text = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
        lang_instr = _language_instruction(user_text)
        lang_prompt = f"{lang_instr}\n\n" + "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages])
        result = await ai_service.ollama_generate(
            prompt=lang_prompt,
            model=model,
        )
        response = result.get("response", "")
        sources = []
        query_type = "general"
        matched_circuits = []

    try:
        last_user_msg = next(
            (m["content"] for m in reversed(messages) if m.get("role") == "user"), ""
        )
        if conversation_id:
            conv = await repo.get(conversation_id)
            if conv and conv.user_id == current_user.id:
                existing = list(conv.messages or [])
                new_msgs = [m for m in messages if m not in existing]
                existing.extend(new_msgs)
                existing.append({"role": "assistant", "content": response, "sources": sources})
                await repo.update(conversation_id, messages=existing)
        else:
            title = (last_user_msg or "New Chat")[:80]
            all_msgs = list(messages)
            all_msgs.append({"role": "assistant", "content": response, "sources": sources})
            conv = await repo.create(
                user_id=current_user.id,
                title=title,
                messages=all_msgs,
                model=model or settings.ollama_model,
            )
            conversation_id = conv.id
    except Exception:
        pass

    return {
        "response": response,
        "model": model or settings.ollama_model,
        "query_type": query_type,
        "sources": sources,
        "matched_circuits": matched_circuits,
        "conversation_id": conversation_id,
    }


@router.post("/chat/stream")
async def chat_stream(body: ChatStreamRequest, current_user: User = Depends(get_current_user)):
    messages = body.messages
    model = body.model
    conversation_id = body.conversation_id

    async def _proxy_stream():
        import httpx as _httpx
        import json as _json

        collected = ""
        meta_info = {}
        final_content = ""
        try:
            async with _httpx.AsyncClient(timeout=120.0) as client:
                ai_url = f"http://{settings.ai_engine_host}:{settings.ai_engine_port}/api/v1/chat"
                payload = {
                    "messages": messages,
                    "model": model or settings.ollama_model,
                    "stream": True,
                    "max_tokens": 2048,
                }
                async with client.stream("POST", ai_url, json=payload) as resp:
                    async for line in resp.aiter_lines():
                        if line.startswith("data: "):
                            raw = line[6:]
                            try:
                                data = _json.loads(raw)
                                t = data.get("type", "")
                                if t == "meta":
                                    meta_info = data
                                elif t == "token":
                                    token = data.get("token", "")
                                    if token:
                                        collected += token
                                        payload = _json.dumps({"type": "token", "token": token})
                                        yield f"data: {payload}\n\n"
                                elif t == "done":
                                    final_content = data.get("content", collected)
                                elif t == "error":
                                    err = _json.dumps({"type": "error", "detail": data.get("detail", "")})
                                    yield f"data: {err}\n\n"
                            except _json.JSONDecodeError:
                                pass
        except Exception:
            user_text = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
            lang_instr = _language_instruction(user_text)
            system = f"You are BreadBoard AI, an expert electronics engineering assistant. {lang_instr}"
            full_messages = [{"role": "system", "content": system}] + messages
            async for line in ai_service.ollama_chat_stream(messages=full_messages, model=model):
                if line.strip():
                    try:
                        data = _json.loads(line)
                        content = data.get("message", {}).get("content", "")
                        if content:
                            collected += content
                            yield f"data: {_json.dumps({'type': 'token', 'token': content})}\n\n"
                        if data.get("done"):
                            final_content = collected
                    except _json.JSONDecodeError:
                        pass

        result_content = final_content or collected
        done_data = {
            "type": "done",
            "content": result_content,
            "meta": meta_info,
            "conversation_id": conversation_id,
        }
        yield f"data: {_json.dumps(done_data)}\n\n"

        if result_content:
            try:
                from app.models.conversation import Conversation as _Conv
                from app.db.base import async_session_factory as _factory
                from app.db.repository import BaseRepository as _Repo

                async with _factory() as db:
                    repo = _Repo(_Conv, db)
                    if conversation_id:
                        conv = await repo.get(conversation_id)
                        if conv and conv.user_id == current_user.id:
                            existing = list(conv.messages or [])
                            existing.append(
                                {
                                    "role": "assistant",
                                    "content": result_content,
                                    "sources": meta_info.get("sources", []),
                                }
                            )
                            await repo.update(conversation_id, messages=existing)
                            await db.commit()
                    else:
                        last_user_msg = next(
                            (m["content"] for m in reversed(messages) if m.get("role") == "user"),
                            "",
                        )
                        title = (last_user_msg or "New Chat")[:80]
                        all_msgs = list(messages)
                        all_msgs.append({"role": "assistant", "content": result_content})
                        conv = await repo.create(
                            user_id=current_user.id,
                            title=title,
                            messages=all_msgs,
                            model=model or settings.ollama_model,
                        )
                        await db.commit()
                        conv_data = _json.dumps({"type": "conv_id", "conversation_id": conv.id})
                        yield f"data: {conv_data}\n\n"
            except Exception:
                pass

    return StreamingResponse(_proxy_stream(), media_type="text/event-stream")


@router.post("/generate")
async def generate(body: GenerateRequest, current_user: User = Depends(get_current_user)):
    prompt = body.prompt
    model = body.model
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
async def generate_circuit(
    body: CircuitGenerateRequest, current_user: User = Depends(get_current_user)
):
    description = body.description

    try:
        result = await ai_service.generate_circuit(description=description)
        response = result.get("response", "")
        sources = result.get("sources", [])
        return {
            "response": response,
            "sources": sources,
        }
    except Exception:
        lang_instr = _language_instruction(description)
        prompt = (
            f"{lang_instr}\n\n"
            f"What parts are needed for: {description}\n\n"
            "Describe each part and how they connect to work together."
        )
        return await ai_service.circuit_generate_with_fallback(prompt=prompt)


@router.post("/speech/stt")
async def transcribe(body: STTRequest, current_user: User = Depends(get_current_user)):
    try:
        return await ai_service.transcribe(
            audio_base64=body.audio,
            language=body.language,
        )
    except Exception:
        return {
            "message": "STT not configured yet",
            "detail": "Install Vosk or Whisper (pip install breadboard-ai-engine[stt,ml])",
        }


@router.post("/speech/tts")
async def synthesize(body: TTSRequest, current_user: User = Depends(get_current_user)):
    try:
        return await ai_service.synthesize(
            text=body.text,
            voice=body.voice,
        )
    except Exception:
        return {"message": "TTS not configured yet"}


@router.post("/vision/detect")
async def detect_components(
    body: VisionDetectRequest, current_user: User = Depends(get_current_user)
):
    try:
        return await ai_service.detect_components(image_base64=body.image)
    except Exception as e:
        detail = str(e)
        logger.warning("Vision detection fallback: %s", detail)
        return {
            "status": "error",
            "message": (
                "Vision detection is not available. "
                "Make sure Ollama is running with a vision-capable model "
                "(e.g., llava, llama3.2-vision) and OLLAMA_VISION_MODEL is set correctly."
            ),
            "detail": detail,
            "fallback": True,
        }


@router.post("/cost/estimate")
async def estimate_cost(body: CostEstimateRequest, current_user: User = Depends(get_current_user)):
    try:
        return await ai_service.estimate_cost(
            components=body.components,
        )
    except Exception:
        return {"message": "Cost estimation not configured yet"}
