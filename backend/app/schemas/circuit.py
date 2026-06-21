from datetime import datetime
from app.schemas.common import BaseSchema


class CircuitCreate(BaseSchema):
    project_id: int | None = None
    name: str
    description: str | None = None
    netlist: str | None = None
    schematic_data: dict | None = None
    components_json: dict | None = None


class CircuitUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None
    netlist: str | None = None
    schematic_data: dict | None = None
    components_json: dict | None = None


class CircuitResponse(BaseSchema):
    id: int
    project_id: int | None
    user_id: int
    name: str
    description: str | None
    netlist: str | None
    schematic_data: dict | None
    components_json: dict | None
    created_at: datetime
    updated_at: datetime


class CircuitList(BaseSchema):
    items: list[CircuitResponse]
    total: int
