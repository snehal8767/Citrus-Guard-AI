"""Metrics service: compute dashboard KPIs from the database."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Alert, Orchard, OrchardZone, Scan, SensorReading


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def compute_metrics(db: Session, orchard_id: int) -> dict:
    orchard = db.get(Orchard, orchard_id)
    if orchard is None:
        raise ValueError(f"Orchard {orchard_id} not found")

    zones = db.query(OrchardZone).filter(OrchardZone.orchard_id == orchard_id).all()
    total_area = orchard.area
    monitored_area = sum(z.area for z in zones)

    healthy_area = sum(z.area for z in zones if z.health_status == "Healthy")
    at_risk_area = sum(z.area for z in zones if z.health_status in ("At Risk", "Watch"))
    critical_zones = sum(1 for z in zones if z.health_status == "Critical")

    active_alerts = (
        db.query(func.count(Alert.id))
        .join(OrchardZone, Alert.zone_id == OrchardZone.id)
        .filter(OrchardZone.orchard_id == orchard_id, Alert.status.notin_(["Resolved", "Rejected"]))
        .scalar()
    )

    latest_scan = (
        db.query(Scan)
        .filter(Scan.orchard_id == orchard_id)
        .order_by(Scan.timestamp.desc())
        .first()
    )

    coverage = round((monitored_area / total_area) * 100, 1) if total_area else 0.0

    # Sensor health: % of zones whose latest reading is within normal range.
    sensor_health = _sensor_health(db, zones)

    return {
        "total_orchard_area": total_area,
        "monitored_area": round(monitored_area, 2),
        "healthy_area": round(healthy_area, 2),
        "at_risk_area": round(at_risk_area, 2),
        "critical_zones": critical_zones,
        "active_alerts": active_alerts,
        "latest_scan": latest_scan.timestamp if latest_scan else None,
        "monitoring_coverage": coverage,
        "sensor_health": sensor_health,
    }


def _sensor_health(db: Session, zones: list[OrchardZone]) -> float:
    if not zones:
        return 0.0
    healthy = 0
    for zone in zones:
        reading = (
            db.query(SensorReading)
            .filter(SensorReading.zone_id == zone.id)
            .order_by(SensorReading.timestamp.desc())
            .first()
        )
        if reading is None:
            continue
        if (
            25 <= reading.soil_moisture <= 45
            and 20 <= reading.temperature <= 35
            and 40 <= reading.humidity <= 75
            and reading.leaf_wetness <= 40
        ):
            healthy += 1
    return round((healthy / len(zones)) * 100, 1)
