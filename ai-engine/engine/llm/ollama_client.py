import httpx
from typing import AsyncGenerator, Optional
from engine.core.config import settings
from .model_registry import ModelInfo


OLLAMA_CHAT_URL = f"{settings.ollama_host}/api/chat"
OLLAMA_GENERATE_URL = f"{settings.ollama_host}/api/generate"
OLLAMA_TAGS_URL = f"{settings.ollama_host}/api/tags"
OLLAMA_PULL_URL = f"{settings.ollama_host}/api/pull"


class OllamaClient:
    """Async client for local Ollama inference."""

    def __init__(self):
        self._client = httpx.AsyncClient(
            timeout=settings.ollama_request_timeout,
            follow_redirects=True,
        )

    async def close(self):
        await self._client.aclose()

    # ── Model Management ───────────────────────────────────────

    async def list_models(self) -> list[dict]:
        resp = await self._client.get(OLLAMA_TAGS_URL)
        resp.raise_for_status()
        return resp.json().get("models", [])

    async def is_model_available(self, model: str) -> bool:
        models = await self.list_models()

        for m in models:
            name = m.get("name", "")

            if name == model:
                return True

            if name.startswith(f"{model}:"):
                return True

        return False

    async def pull_model(self, model: str) -> AsyncGenerator[dict, None]:
        async with self._client.stream("POST", OLLAMA_PULL_URL, json={"name": model}) as resp:
            async for line in resp.aiter_lines():
                if line.strip():
                    import json as _json
                    yield _json.loads(line)

    # ── Chat (for Qwen3, Gemma — instruction-following) ────────

    async def chat(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False,
    ) -> AsyncGenerator[dict, None]:
        payload = {
            "model": model,
            "messages": messages,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "stream": stream,
        }
        if stream:
            async with self._client.stream("POST", OLLAMA_CHAT_URL, json=payload) as resp:
                async for line in resp.aiter_lines():
                    if line.strip():
                        import json as _json
                        yield _json.loads(line)
        else:
            resp = await self._client.post(OLLAMA_CHAT_URL, json=payload)
            resp.raise_for_status()
            yield resp.json()

    async def chat_sync(self, model: str, messages: list[dict], **kwargs) -> str:
        """Convenience: returns just the content string."""
        async for chunk in self.chat(model, messages, stream=False, **kwargs):
            return chunk.get("message", {}).get("content", "")

    # ── Generate (for DeepSeek Coder — completions) ────────────

    async def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "stream": False,
        }
        resp = await self._client.post(OLLAMA_GENERATE_URL, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")

    # ── Smart Dispatch ─────────────────────────────────────────

    async def dispatch(
        self,
        model_info: ModelInfo,
        messages: list[dict],
        prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> str:
        """Route to chat or generate based on model capabilities."""
        tag = model_info.ollama_tag or model_info.name
        if "coder" in model_info.name.lower() and prompt:
            return await self.generate(tag, prompt, temperature, max_tokens)
        return await self.chat_sync(tag, messages, temperature=temperature, max_tokens=max_tokens)


# Singleton
client = OllamaClient()
