from datetime import datetime
from sqlalchemy import (
    String, Text, DateTime, Integer, Boolean, Float,
    ForeignKey, UniqueConstraint, Index, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum


class SourceType(str, enum.Enum):
    WIKIPEDIA = "wikipedia"
    ELECTRONICS_TUTORIALS = "electronics_tutorials"
    ARDUINO_DOCS = "arduino_docs"
    RASPBERRY_PI_DOCS = "raspberry_pi_docs"
    SPARKFUN = "sparkfun"
    ADAFRUIT = "adafruit"
    OPEN_SOURCE_CIRCUIT = "open_source_circuit"
    WIKIPEDIA_COMMONS = "wikipedia_commons"
    WIKIMEDIA_COMMONS = "wikimedia_commons"
    DATASHEET = "datasheet"
    ACADEMIC = "academic"
    OTHER = "other"


class ContentType(str, enum.Enum):
    CIRCUIT = "circuit"
    COMPONENT = "component"
    LESSON = "lesson"
    REPAIR_GUIDE = "repair_guide"
    SAFETY_CHECK = "safety_check"
    COST_ESTIMATE = "cost_estimate"
    BREADBOARD_LAYOUT = "breadboard_layout"
    TUTORIAL = "tutorial"
    EXPLANATION = "explanation"
    IMAGE = "image"
    DATASHEET = "datasheet"
    CODE_EXAMPLE = "code_example"
    SCHEMATIC = "schematic"


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # reduced size for MySQL unique index
    url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    # store enum as string
    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=5
    )

    license: Mapped[str | None] = mapped_column(
        String(255)
    )

    author: Mapped[str | None] = mapped_column(
        String(255)
    )

    description: Mapped[str | None] = mapped_column(
        Text
    )

    language: Mapped[str] = mapped_column(
        String(10),
        default="en"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    last_validated_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    content_links = relationship(
        "ContentSource",
        back_populates="source",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_source_type", "source_type"),
        Index("idx_source_priority", "priority"),
        Index("idx_source_active", "is_active"),
    )


class ContentSource(Base):
    __tablename__ = "content_sources"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sources.id"),
        nullable=False
    )

    content_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    content_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    usage_context: Mapped[str | None] = mapped_column(
        String(255)
    )

    attribution_text: Mapped[str | None] = mapped_column(
        Text
    )

    image_url: Mapped[str | None] = mapped_column(
        String(255)
    )

    relevance_score: Mapped[float | None] = mapped_column(
        Float
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    source = relationship(
        "Source",
        back_populates="content_links"
    )

    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "content_type",
            "content_id",
            name="uk_content_source"
        ),
        Index(
            "idx_content_type_id",
            "content_type",
            "content_id"
        ),
        Index(
            "idx_content_source",
            "source_id",
            "content_type"
        ),
    )
