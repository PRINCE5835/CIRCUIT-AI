from datetime import datetime
from app.schemas.common import BaseSchema


class ConversationCreate(BaseSchema):
    title: str = "New Chat"
    messages: list = []
    model: str | None = None


class ConversationUpdate(BaseSchema):
    title: str | None = None
    messages: list | None = None
    model: str | None = None


class AddMessageRequest(BaseSchema):
    role: str
    content: str


class ConversationResponse(BaseSchema):
    id: int
    user_id: int
    title: str
    messages: list
    model: str | None
    created_at: datetime
    updated_at: datetime


class ConversationSummary(BaseSchema):
    id: int
    user_id: int
    title: str
    model: str | None
    message_count: int
    created_at: datetime
    updated_at: datetime


class ConversationList(BaseSchema):
    items: list[ConversationSummary]
    total: int
