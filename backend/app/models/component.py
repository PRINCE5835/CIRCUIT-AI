from datetime import datetime
from sqlalchemy import String, Text, DateTime, JSON, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Component(Base):
    __tablename__ = "components"

    __table_args__ = (
        Index("idx_component_category", "category"),
        Index("idx_component_name", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory: Mapped[str | None] = mapped_column(String(100))
    manufacturer: Mapped[str | None] = mapped_column(String(255))
    model_number: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    specifications_json: Mapped[dict | None] = mapped_column(JSON)
    datasheet_url: Mapped[str | None] = mapped_column(String(500))
    image_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    listings = relationship("MarketplaceListing", back_populates="component")
