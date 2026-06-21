from datetime import datetime
from app.schemas.common import BaseSchema


class ComponentCreate(BaseSchema):
    name: str
    category: str
    subcategory: str | None = None
    manufacturer: str | None = None
    model_number: str | None = None
    specifications_json: dict | None = None
    datasheet_url: str | None = None
    image_url: str | None = None


class ComponentUpdate(BaseSchema):
    name: str | None = None
    category: str | None = None
    subcategory: str | None = None
    manufacturer: str | None = None
    model_number: str | None = None
    specifications_json: dict | None = None
    datasheet_url: str | None = None
    image_url: str | None = None


class ComponentResponse(BaseSchema):
    id: int
    name: str
    category: str
    subcategory: str | None
    manufacturer: str | None
    model_number: str | None
    specifications_json: dict | None
    datasheet_url: str | None
    image_url: str | None
    created_at: datetime


class ComponentList(BaseSchema):
    items: list[ComponentResponse]
    total: int
