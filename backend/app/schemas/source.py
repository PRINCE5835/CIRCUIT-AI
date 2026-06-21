from datetime import datetime
from pydantic import BaseModel, Field

# ── Source ────────────────────────────────────────────────────


class SourceBase(BaseModel):
    title: str = Field(..., max_length=255)
    url: str = Field(..., max_length=1000)
    source_type: str = Field(...)
    priority: int = Field(default=5, ge=1, le=10)
    license: str | None = None
    author: str | None = None
    description: str | None = None
    language: str = "en"
    is_active: bool = True


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    title: str | None = None
    url: str | None = None
    source_type: str | None = None
    priority: int | None = Field(default=None, ge=1, le=10)
    license: str | None = None
    author: str | None = None
    description: str | None = None
    language: str | None = None
    is_active: bool | None = None


class SourceResponse(SourceBase):
    id: int
    last_validated_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SourceList(BaseModel):
    items: list[SourceResponse]
    total: int


# ── ContentSource (junction) ──────────────────────────────────


class ContentSourceBase(BaseModel):
    source_id: int
    content_type: str = Field(...)
    content_id: int
    usage_context: str | None = None
    attribution_text: str | None = None
    image_url: str | None = None
    relevance_score: float | None = Field(default=None, ge=0.0, le=1.0)


class ContentSourceCreate(ContentSourceBase):
    pass


class ContentSourceResponse(ContentSourceBase):
    id: int
    created_at: datetime
    source: SourceResponse | None = None

    model_config = {"from_attributes": True}


class ContentSourceList(BaseModel):
    items: list[ContentSourceResponse]
    total: int


# ── Attribution (for AI output) ───────────────────────────────


class SourceAttribution(BaseModel):
    """Structured attribution for AI-generated content."""

    source_title: str
    source_url: str
    source_type: str
    license: str | None = None
    attribution_text: str
    image_url: str | None = None


class AttributedContent(BaseModel):
    """Wrapper for any AI-generated content with source links."""

    content: str
    sources: list[SourceAttribution]
