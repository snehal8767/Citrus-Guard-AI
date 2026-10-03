"""Intervention model."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.engine import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Intervention(Base):
    __tablename__ = "interventions"

    id: Mapped[int] = mapped_column(primary_key=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("orchard_zones.id", ondelete="CASCADE"), index=True)
    intervention_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_area: Mapped[float] = mapped_column(Float, nullable=False)  # acres
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="Planned")
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
