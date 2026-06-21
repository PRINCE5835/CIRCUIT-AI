from datetime import datetime
from app.schemas.common import BaseSchema


class ProjectCreate(BaseSchema):
    title: str
    description: str | None = None
    circuit_data: dict | None = None
    is_public: bool = False


class ProjectUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    circuit_data: dict | None = None
    status: str | None = None
    is_public: bool | None = None


class ProjectResponse(BaseSchema):
    id: int
    user_id: int
    title: str
    description: str | None
    circuit_data: dict | None
    breadboard_image_url: str | None
    status: str
    is_public: bool
    created_at: datetime
    updated_at: datetime


class ProjectList(BaseSchema):
    items: list[ProjectResponse]
    total: int
