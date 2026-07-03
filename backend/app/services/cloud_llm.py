import json

import httpx

from app.core.config import settings


class CloudLLM:
    def __init__(self):
        self.api_key = settings.google_api_key
        self.model = settings.gemini_model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self._available = bool(self.api_key)

    @property
    def is_available(self) -> bool:
        return self._available

    def _build_contents(self, messages: list[dict]) -> list[dict]:
        contents = []
        for m in messages:
            role = "model" if m.get("role") == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": m.get("content", "")}]})
        return contents

    async def generate(self, prompt: str, system: str | None = None) -> str:
        if not self._available:
            raise RuntimeError(
                "Google API key not configured. Set GOOGLE_API_KEY environment variable."
            )
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        body = {"contents": [{"parts": [{"text": prompt}]}]}
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, json=body)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    async def chat(self, messages: list[dict], system: str | None = None) -> str:
        if not self._available:
            raise RuntimeError("Google API key not configured")
        contents = self._build_contents(messages)
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        body = {"contents": contents}
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(url, json=body)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    async def chat_stream(self, messages: list[dict], system: str | None = None):
        if not self._available:
            raise RuntimeError("Google API key not configured")
        contents = self._build_contents(messages)
        url = f"{self.base_url}/models/{self.model}:streamGenerateContent?alt=sse&key={self.api_key}"
        body = {"contents": contents}
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        full_text = ""
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream("POST", url, json=body) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.startswith("data: "):
                        raw = line[6:]
                        if raw.strip() in ("", "[DONE]"):
                            continue
                        try:
                            data = json.loads(raw)
                            candidates = data.get("candidates", [])
                            if candidates:
                                parts = candidates[0].get("content", {}).get("parts", [])
                                for part in parts:
                                    token = part.get("text", "")
                                    if token:
                                        full_text += token
                                        yield f"data: {json.dumps({'type': 'token', 'token': token})}\n\n"
                        except json.JSONDecodeError:
                            pass
        yield f"data: {json.dumps({'type': 'done', 'content': full_text})}\n\n"

    async def health(self) -> dict:
        if not self._available:
            return {"status": "unhealthy", "cloud_llm": False, "detail": "GOOGLE_API_KEY not set"}
        try:
            url = f"{self.base_url}/models?key={self.api_key}"
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                count = len(data.get("models", []))
                return {"status": "healthy", "cloud_llm": True, "models_available": count}
        except Exception as e:
            return {"status": "unhealthy", "cloud_llm": False, "detail": str(e)}


cloud_llm = CloudLLM()
