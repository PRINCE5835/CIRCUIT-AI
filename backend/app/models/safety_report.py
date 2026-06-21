from datetime import datetime
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class SafetyReport(Base):
    __tablename__ = "safety_reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    circuit_id: Mapped[int] = mapped_column(Integer, ForeignKey("circuits.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    issues_json: Mapped[dict | None] = mapped_column(JSON)
    severity: Mapped[str | None] = mapped_column(String(20))
    recommendations: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    circuit = relationship("Circuit", back_populates="safety_reports")
    user = relationship("User", back_populates="safety_reports")
