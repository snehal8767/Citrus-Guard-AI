"""HistoricalMonitoring model."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.engine import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class HistoricalMonitoring(Base):
    __tablename__ = "historical_monitoring"

    id: Mapped[int] = mapped_column(primary_key=True)
    orchard_id: Mapped[int] = mapped_column(ForeignKey("orchards.id", ondelete="CASCADE"), index=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("orchard_zones.id", ondelete="CASCADE"), index=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id", ondelete="SET NULL"), nullable=True)
    health_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    affected_area: Mapped[float] = mapped_column(Float, nullable=False)  # acres
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
