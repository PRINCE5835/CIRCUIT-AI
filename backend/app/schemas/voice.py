from datetime import datetime
from app.schemas.common import BaseSchema


class VoiceSessionCreate(BaseSchema):
    session_type: str
    audio_url: str | None = None
    transcript: str | None = None
    language: str = "en"
    duration_ms: int | None = None
    processed_json: dict | None = None


class VoiceSessionResponse(BaseSchema):
    id: int
    user_id: int
    session_type: str
    audio_url: str | None
    transcript: str | None
    language: str
    duration_ms: int | None
    processed_json: dict | None
    created_at: datetime


class VoiceSessionList(BaseSchema):
    items: list[VoiceSessionResponse]
    total: int
