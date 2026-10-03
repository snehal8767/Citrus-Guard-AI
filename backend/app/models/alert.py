"""Alert and FarmerVerification models."""
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = (
        CheckConstraint("risk_score >= 0 AND risk_score <= 100", name="ck_alert_risk_score"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("orchard_zones.id", ondelete="CASCADE"), index=True)
    alert_type: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="New")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)

    zone: Mapped["OrchardZone"] = relationship(lazy="selectin")
    verifications: Mapped[list["FarmerVerification"]] = relationship(
        back_populates="alert", cascade="all, delete-orphan", lazy="selectin"
    )


class FarmerVerification(Base):
    __tablename__ = "farmer_verifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id", ondelete="CASCADE"), index=True)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)  # verify | reject | rescan
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    alert: Mapped["Alert"] = relationship(back_populates="verifications")
