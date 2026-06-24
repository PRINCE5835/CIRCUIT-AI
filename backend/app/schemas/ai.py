from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    messages: list[dict] = Field(..., min_length=1)
    model: str | None = None
    conversation_id: int | None = None


class ChatStreamRequest(BaseModel):
    messages: list[dict] = Field(..., min_length=1)
    model: str | None = None
    conversation_id: int | None = None


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model: str | None = None


class CircuitGenerateRequest(BaseModel):
    description: str = Field(..., min_length=1)
    model: str | None = None


class STTRequest(BaseModel):
    audio: str = Field(..., min_length=1)
    language: str = "en"


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1)
    voice: str = "default"


class VisionDetectRequest(BaseModel):
    image: str = Field(..., min_length=1)


class CostEstimateRequest(BaseModel):
    components: list = Field(..., min_length=1)
