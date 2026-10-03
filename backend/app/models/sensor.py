"""SensorReading model."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.engine import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("orchard_zones.id", ondelete="CASCADE"), index=True)
    soil_moisture: Mapped[float] = mapped_column(Float, nullable=False)  # percent
    temperature: Mapped[float] = mapped_column(Float, nullable=False)  # deg C
    humidity: Mapped[float] = mapped_column(Float, nullable=False)  # percent
    leaf_wetness: Mapped[float] = mapped_column(Float, nullable=False)  # percent
    irrigation_status: Mapped[str] = mapped_column(String(32), nullable=False, default="Off")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
