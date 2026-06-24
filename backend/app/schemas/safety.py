from datetime import datetime
from app.schemas.common import BaseSchema


class SafetyReportCreate(BaseSchema):
    circuit_id: int
    status: str = "pending"
    issues_json: dict | None = None
    severity: str | None = None
    recommendations: str | None = None


class SafetyReportUpdate(BaseSchema):
    status: str | None = None
    issues_json: dict | None = None
    severity: str | None = None
    recommendations: str | None = None


class SafetyReportResponse(BaseSchema):
    id: int
    circuit_id: int
    user_id: int
    status: str
    issues_json: dict | None
    severity: str | None
    recommendations: str | None
    created_at: datetime
    updated_at: datetime


class SafetyReportList(BaseSchema):
    items: list[SafetyReportResponse]
    total: int
