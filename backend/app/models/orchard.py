"""Orchard and OrchardZone models."""
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Orchard(Base):
    __tablename__ = "orchards"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    area: Mapped[float] = mapped_column(Float, nullable=False)  # acres
    crop: Mapped[str] = mapped_column(String(64), nullable=False, default="Orange (Nagpur Santra)")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    zones: Mapped[list["OrchardZone"]] = relationship(
        back_populates="orchard", cascade="all, delete-orphan", lazy="selectin"
    )


class OrchardZone(Base):
    __tablename__ = "orchard_zones"
    __table_args__ = (
        CheckConstraint("risk_score >= 0 AND risk_score <= 100", name="ck_zone_risk_score"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    orchard_id: Mapped[int] = mapped_column(ForeignKey("orchards.id", ondelete="CASCADE"), index=True)
    zone_name: Mapped[str] = mapped_column(String(64), nullable=False)
    area: Mapped[float] = mapped_column(Float, nullable=False)  # acres
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    health_status: Mapped[str] = mapped_column(String(32), nullable=False, default="Healthy")
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    orchard: Mapped["Orchard"] = relationship(back_populates="zones")
