from datetime import datetime
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class TimestampSchema(BaseSchema):
    created_at: datetime
    updated_at: datetime


class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=200)


class PaginatedResponse(BaseSchema):
    items: list
    total: int
    skip: int
    limit: int


class APIResponse(BaseSchema):
    success: bool = True
    data: dict | list | None = None
    message: str | None = None


class ErrorResponse(BaseSchema):
    detail: str
    code: str = "internal_error"
