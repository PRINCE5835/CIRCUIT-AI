from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.services.ai_service import ai_service
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.db.repository import BaseRepository

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
async def chat(
    body: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="Messages are required")

    model = body.get("model")
    conversation_id = body.get("conversation_id")
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
        prompt = "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages])
        result = await ai_service.ollama_generate(
            prompt=prompt,
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
async def chat_stream(body: dict, current_user: User = Depends(get_current_user)):
    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="Messages are required")

    model = body.get("model")
    conversation_id = body.get("conversation_id")

    async def _proxy_stream():
        import httpx as _httpx
        import json as _json
        ai_url = f"http://{settings.ai_engine_host}:{settings.ai_engine_port}/api/v1/chat"
        payload = {
            "messages": messages,
            "model": model or settings.ollama_model,
            "stream": True,
            "max_tokens": 2048,
        }
        collected = ""
        final_content = ""
        meta_info = {}
        try:
            async with _httpx.AsyncClient(timeout=120.0) as client:
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
                                        payload = _json.dumps({'type': 'token', 'token': token})
                                        yield f"data: {payload}\n\n"
                                elif t == "done":
                                    final_content = data.get("content", collected)
                                elif t == "error":
                                    yield f"data: {_json.dumps({'type': 'error', 'detail': data.get('detail', '')})}\n\n"
                            except _json.JSONDecodeError:
                                pass
        except Exception as e:
            yield f"data: {_json.dumps({'type': 'error', 'detail': str(e)})}\n\n"

        result_content = final_content or collected
        yield f"data: {_json.dumps({'type': 'done', 'content': result_content, 'meta': meta_info, 'conversation_id': conversation_id})}\n\n"

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
                            existing.append({"role": "assistant", "content": result_content, "sources": meta_info.get("sources", [])})
                            await repo.update(conversation_id, messages=existing)
                            await db.commit()
                    else:
                        last_user_msg = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
                        title = (last_user_msg or "New Chat")[:80]
                        all_msgs = list(messages)
                        all_msgs.append({"role": "assistant", "content": result_content})
                        conv = await repo.create(
                            user_id=current_user.id, title=title,
                            messages=all_msgs, model=model or settings.ollama_model,
                        )
                        await db.commit()
                        yield f"data: {_json.dumps({'type': 'conv_id', 'conversation_id': conv.id})}\n\n"
            except Exception:
                pass

    return StreamingResponse(_proxy_stream(), media_type="text/event-stream")


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
        return {"message": "STT not configured yet", "detail": "Install Vosk or Whisper (pip install breadboard-ai-engine[stt,ml])"}


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
    image_base64 = body.get("image", "")
    if not image_base64:
        raise HTTPException(status_code=400, detail="image is required")

    try:
        return await ai_service.detect_components(image_base64=image_base64)
    except Exception:
        prompt = (
            "You are an expert electronics component analyzer. Carefully examine the provided image.\n\n"
            "RULES:\n"
            "- If NO circuit board, electronic components, or electronic parts are visible, respond ONLY with: "
            "NO_CIRCUIT\n"
            "- If the image is blurry, unclear, or too dark to identify components, respond ONLY with: "
            "UNCLEAR\n"
            "- If components ARE visible, list EACH component with as much detail as possible. "
            "For each: name, type (resistor/capacitor/IC/transistor/etc), confidence, quantity, package type, markings.\n"
            "Format: one component per line: name | type | confidence | quantity | package | markings\n"
            "Be precise about values (e.g., '220Ω Resistor' not just 'Resistor')."
        )
        result = await ai_service.ollama_generate(
            prompt=f"{prompt}\n[Image provided, analyze it]",
            model="llava",
        )
        raw = result.get("response", "")
        raw_upper = raw.strip().upper()
        if raw_upper.startswith("NO_CIRCUIT"):
            return {"status": "no_circuit", "message": "No electronic circuit or components detected in the image.", "model": "llava", "fallback": True}
        if raw_upper.startswith("UNCLEAR"):
            return {"status": "unclear", "message": "The image is not clear enough. Please capture a clearer photo with good lighting.", "model": "llava", "fallback": True}
        try:
            import json as _json
            components = _json.loads(raw)
            if isinstance(components, list):
                return {"status": "success", "components": components, "model": "llava", "fallback": True}
        except Exception:
            pass
        return {"status": "success", "components": [{"name": raw[:200], "type": "unknown", "confidence": 0.5, "quantity": 1}], "model": "llava", "fallback": True}


@router.post("/cost/estimate")
async def estimate_cost(body: dict, current_user: User = Depends(get_current_user)):
    try:
        return await ai_service.estimate_cost(
            components=body.get("components", []),
        )
    except Exception:
        return {"message": "Cost estimation not configured yet"}
