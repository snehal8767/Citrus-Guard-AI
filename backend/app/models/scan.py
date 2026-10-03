"""Scan and AIDetection models."""
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(primary_key=True)
    orchard_id: Mapped[int] = mapped_column(ForeignKey("orchards.id", ondelete="CASCADE"), index=True)
    scan_type: Mapped[str] = mapped_column(String(64), nullable=False, default="drone_simulation")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # percent
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="Completed")

    detections: Mapped[list["AIDetection"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan", lazy="selectin"
    )


class AIDetection(Base):
    __tablename__ = "ai_detections"
    __table_args__ = (
        CheckConstraint("confidence >= 0 AND confidence <= 100", name="ck_detection_confidence"),
        CheckConstraint(
            "severity IN ('Low','Medium','High','Critical')", name="ck_detection_severity"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id", ondelete="CASCADE"), index=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("orchard_zones.id", ondelete="CASCADE"), index=True)
    condition: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    scan: Mapped["Scan"] = relationship(back_populates="detections")
    zone: Mapped["OrchardZone"] = relationship(lazy="selectin")
