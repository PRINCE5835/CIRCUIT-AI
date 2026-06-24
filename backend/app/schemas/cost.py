from datetime import datetime
from app.schemas.common import BaseSchema


class CostEstimateCreate(BaseSchema):
    project_id: int
    total_cost: float | None = None
    currency: str = "USD"
    breakdown_json: dict | None = None


class CostEstimateResponse(BaseSchema):
    id: int
    project_id: int
    user_id: int
    total_cost: float | None
    currency: str
    breakdown_json: dict | None
    created_at: datetime
    updated_at: datetime
