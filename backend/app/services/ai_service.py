import httpx
from fastapi import HTTPException, status

from app.core.config import settings


class AIService:
    def __init__(self):
        self.base_url = f"http://{settings.ai_engine_host}:{settings.ai_engine_port}"
        self.client = httpx.AsyncClient(timeout=60.0)

        self.ollama_base_url = settings.ollama_host
        self.ollama_client = httpx.AsyncClient(timeout=settings.ollama_timeout)

    async def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="AI Engine request timed out",
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"AI Engine error: {e.response.text}",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"AI Engine unreachable: {str(e)}",
            )

    async def health(self) -> dict:
        return await self._request("GET", "/health")

    async def list_models(self) -> dict:
        return await self._request("GET", "/api/v1/models")

    async def get_primary_model(self) -> dict:
        return await self._request("GET", "/api/v1/models/primary")

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        body = {"messages": messages, "max_tokens": 512}
        if model:
            body["model"] = model
        return await self._request("POST", "/api/v1/chat", json=body)

    async def generate(self, prompt: str, model: str | None = None) -> dict:
        body = {"prompt": prompt}
        if model:
            body["model"] = model
        return await self._request("POST", "/api/v1/generate", json=body)

    async def transcribe(self, audio_base64: str, language: str = "en") -> dict:
        return await self._request(
            "POST",
            "/api/v1/speech/stt",
            json={"audio": audio_base64, "language": language},
        )

    async def synthesize(self, text: str, voice: str = "default") -> dict:
        return await self._request(
            "POST",
            "/api/v1/speech/tts",
            json={"text": text, "voice": voice},
        )

    async def detect_components(self, image_base64: str) -> dict:
        return await self._request(
            "POST",
            "/api/v1/vision/detect",
            json={"image": image_base64},
        )

    async def generate_circuit(self, description: str) -> dict:
        return await self._request(
            "POST",
            "/api/v1/circuit/generate",
            json={"description": description},
        )

    async def estimate_cost(self, components: list[dict]) -> dict:
        return await self._request(
            "POST",
            "/api/v1/cost/estimate",
            json={"components": components},
        )

    async def _ollama_request(self, method: str, path: str, **kwargs) -> dict:
        url = f"{self.ollama_base_url}{path}"
        try:
            response = await self.ollama_client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Ollama request timed out",
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Ollama error: {e.response.text}",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Ollama unreachable: {str(e)}",
            )

    async def ollama_health(self) -> dict:
        try:
            tags = await self._ollama_request("GET", "/api/tags")
            return {"status": "healthy", "ollama": True, "models": len(tags.get("models", []))}
        except Exception:
            return {"status": "unhealthy", "ollama": False}

    async def ollama_generate(self, prompt: str, model: str | None = None, **kwargs) -> dict:
        body = {
            "model": model or settings.ollama_model,
            "prompt": prompt,
            "stream": False,
            **kwargs,
        }
        return await self._ollama_request("POST", "/api/generate", json=body)


ai_service = AIService()
