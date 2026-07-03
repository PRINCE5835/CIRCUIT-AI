import json
from typing import AsyncGenerator

import httpx

from app.core.config import settings


class GroqProvider:
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.model = settings.groq_model
        self.base_url = "https://api.groq.com/openai/v1"
        self._available = bool(self.api_key)

    @property
    def is_available(self) -> bool:
        return self._available

    async def chat(self, messages: list[dict], system: str | None = None) -> str:
        if not self._available:
            raise RuntimeError("Groq API key not configured")
        full_messages = list(messages)
        if system:
            full_messages.insert(0, {"role": "system", "content": system})
        body = {
            "model": self.model,
            "messages": full_messages,
            "stream": False,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.base_url}/chat/completions"
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(url, json=body, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    async def generate(self, prompt: str, system: str | None = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages=messages, system=system)

    async def chat_stream(self, messages: list[dict], system: str | None = None):
        if not self._available:
            raise RuntimeError("Groq API key not configured")
        full_messages = list(messages)
        if system:
            full_messages.insert(0, {"role": "system", "content": system})
        body = {
            "model": self.model,
            "messages": full_messages,
            "stream": True,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.base_url}/chat/completions"
        full_text = ""
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream("POST", url, json=body, headers=headers) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.startswith("data: "):
                        raw = line[6:]
                        if raw.strip() == "[DONE]":
                            continue
                        try:
                            data = json.loads(raw)
                            delta = data.get("choices", [{}])[0].get("delta", {})
                            token = delta.get("content", "")
                            if token:
                                full_text += token
                                yield f"data: {json.dumps({'type': 'token', 'token': token})}\n\n"
                        except json.JSONDecodeError:
                            pass
        yield f"data: {json.dumps({'type': 'done', 'content': full_text})}\n\n"

    async def health(self) -> dict:
        if not self._available:
            return {"status": "unhealthy", "groq": False, "detail": "GROQ_API_KEY not set"}
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            url = f"{self.base_url}/models"
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                count = len(data)
                return {"status": "healthy", "groq": True, "models_available": count}
        except Exception as e:
            return {"status": "unhealthy", "groq": False, "detail": str(e)}


class GeminiProvider:
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

    async def generate(self, prompt: str, system: str | None = None) -> str:
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        body = {"contents": [{"parts": [{"text": prompt}]}]}
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        async with httpx.AsyncClient(timeout=60) as client:
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
            return {"status": "unhealthy", "gemini": False, "detail": "GOOGLE_API_KEY not set"}
        try:
            url = f"{self.base_url}/models?key={self.api_key}"
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                count = len(data.get("models", []))
                return {"status": "healthy", "gemini": True, "models_available": count}
        except Exception as e:
            return {"status": "unhealthy", "gemini": False, "detail": str(e)}


class CloudLLM:
    def __init__(self):
        self.groq = GroqProvider()
        self.gemini = GeminiProvider()

    @property
    def is_available(self) -> bool:
        return self.groq.is_available or self.gemini.is_available

    async def generate(self, prompt: str, system: str | None = None) -> str | None:
        if self.groq.is_available:
            try:
                return await self.groq.generate(prompt=prompt, system=system)
            except Exception:
                pass
        if self.gemini.is_available:
            try:
                return await self.gemini.generate(prompt=prompt, system=system)
            except Exception:
                pass
        return None

    async def chat(self, messages: list[dict], system: str | None = None) -> str | None:
        if self.groq.is_available:
            try:
                return await self.groq.chat(messages=messages, system=system)
            except Exception:
                pass
        if self.gemini.is_available:
            try:
                return await self.gemini.chat(messages=messages, system=system)
            except Exception:
                pass
        return None

    async def chat_stream(self, messages: list[dict], system: str | None = None):
        if self.groq.is_available:
            try:
                async for chunk in self.groq.chat_stream(messages=messages, system=system):
                    yield chunk
                return
            except Exception:
                pass
        if self.gemini.is_available:
            try:
                async for chunk in self.gemini.chat_stream(messages=messages, system=system):
                    yield chunk
                return
            except Exception:
                pass

    async def health(self) -> dict:
        if self.groq.is_available:
            return await self.groq.health()
        if self.gemini.is_available:
            return await self.gemini.health()
        return {"status": "unhealthy", "detail": "No cloud LLM configured (set GROQ_API_KEY or GOOGLE_API_KEY)"}


cloud_llm = CloudLLM()
