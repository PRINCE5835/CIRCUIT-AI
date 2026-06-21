from datetime import datetime
from pydantic import EmailStr, field_validator

from app.schemas.common import BaseSchema


class UserCreate(BaseSchema):
    email: EmailStr
    username: str
    password: str
    display_name: str | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserUpdate(BaseSchema):
    display_name: str | None = None
    preferred_language: str | None = None
    avatar_url: str | None = None


class UserResponse(BaseSchema):
    id: int
    email: str
    username: str
    display_name: str | None
    avatar_url: str | None
    preferred_language: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
