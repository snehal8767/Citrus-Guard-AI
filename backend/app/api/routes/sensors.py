"""Sensor routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import OrchardZone, SensorReading, User
from app.schemas.sensor import SensorReadingResponse, SensorStatus

router = APIRouter(prefix="/sensors", tags=["sensors"])

# Normal ranges for status classification.
RANGES = {
    "soil_moisture": (25, 45),
    "temperature": (20, 35),
    "humidity": (40, 75),
    "leaf_wetness": (0, 40),
}


def _status_for(reading: SensorReading) -> str:
    checks = [
        RANGES["soil_moisture"][0] <= reading.soil_moisture <= RANGES["soil_moisture"][1],
        RANGES["temperature"][0] <= reading.temperature <= RANGES["temperature"][1],
        RANGES["humidity"][0] <= reading.humidity <= RANGES["humidity"][1],
        reading.leaf_wetness <= RANGES["leaf_wetness"][1],
    ]
    failed = checks.count(False)
    if failed == 0:
        return "Normal"
    if failed == 1:
        return "Warning"
    return "Critical"


@router.get("", response_model=list[SensorReadingResponse])
def list_readings(
    zone_id: int | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(SensorReading)
    if zone_id is not None:
        query = query.filter(SensorReading.zone_id == zone_id)
    return query.order_by(SensorReading.timestamp.desc()).limit(limit).all()


@router.get("/status", response_model=list[SensorStatus])
def sensor_status(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Latest reading per zone with a Normal/Warning/Critical status."""
    zones = db.query(OrchardZone).all()
    out = []
    for zone in zones:
        reading = (
            db.query(SensorReading)
            .filter(SensorReading.zone_id == zone.id)
            .order_by(SensorReading.timestamp.desc())
            .first()
        )
        if reading is None:
            continue
        out.append(
            SensorStatus(
                zone_id=zone.id,
                zone_name=zone.zone_name,
                soil_moisture=reading.soil_moisture,
                temperature=reading.temperature,
                humidity=reading.humidity,
                leaf_wetness=reading.leaf_wetness,
                irrigation_status=reading.irrigation_status,
                status=_status_for(reading),
                last_updated=reading.timestamp,
            )
        )
    return out
