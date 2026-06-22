from datetime import datetime
from app.schemas.common import BaseSchema


class BOMItemCreate(BaseSchema):
    component_id: int
    quantity: int = 1
    notes: str | None = None


class BOMItemUpdate(BaseSchema):
    quantity: int | None = None
    notes: str | None = None


class BOMItemResponse(BaseSchema):
    id: int
    project_id: int
    component_id: int
    quantity: int
    notes: str | None
    created_at: datetime
    component_name: str | None = None
    component_category: str | None = None


class BOMResponse(BaseSchema):
    items: list[BOMItemResponse]
    total: int
    project_id: int
