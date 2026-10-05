"""Zone recommendation builder.

Produces a structured, dosage-free action plan for a zone:
condition, risk, affected area, 5 fixed steps, and a safety note.
Never prescribes pesticides, doses, or chemicals.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import AIDetection, Alert, HistoricalMonitoring, OrchardZone

STEPS = [
    "Step 1: Inspect affected trees and confirm the suspected condition.",
    "Step 2: If confirmed, consult the recommended agricultural treatment/advisory.",
    "Step 3: Generate a targeted intervention map for the affected area only.",
    "Step 4: Apply the approved treatment only to the verified affected zone.",
    "Step 5: Re-scan the zone after intervention to confirm recovery.",
]

SAFETY_NOTE = (
    "This website does not automatically prescribe a pesticide, dose, or chemical. "
    "Always follow licensed agricultural advice and local regulations."
)

FALLBACK_CONDITION = "Suspected disease/stress"


def build_recommendation(db: Session, zone_id: int) -> dict:
    zone = db.get(OrchardZone, zone_id)
    if zone is None:
        raise ValueError(f"Zone {zone_id} not found")

    detection = (
        db.query(AIDetection)
        .filter(AIDetection.zone_id == zone_id)
        .order_by(AIDetection.timestamp.desc())
        .first()
    )
    latest_alert = (
        db.query(Alert)
        .filter(Alert.zone_id == zone_id)
        .order_by(Alert.created_at.desc())
        .first()
    )
    latest_history = (
        db.query(HistoricalMonitoring)
        .filter(HistoricalMonitoring.zone_id == zone_id)
        .order_by(HistoricalMonitoring.recorded_at.desc())
        .first()
    )

    condition = detection.condition if detection else FALLBACK_CONDITION
    severity = detection.severity if detection else "Unknown"
    if latest_history and latest_history.affected_area:
        affected_area = round(latest_history.affected_area, 2)
    else:
        affected_area = round(zone.area, 2) if zone.health_status != "Healthy" else 0.0

    return {
        "zone_id": zone.id,
        "zone_name": zone.zone_name,
        "health_status": zone.health_status,
        "risk_score": zone.risk_score,
        "area": zone.area,
        "condition": condition,
        "severity": severity,
        "risk": zone.risk_score,
        "affected_area": affected_area,
        "alert_id": latest_alert.id if latest_alert else None,
        "alert_status": latest_alert.status if latest_alert else None,
        "verified_alert": latest_alert.status == "Verified" if latest_alert else False,
        "steps": STEPS,
        "safety_note": SAFETY_NOTE,
    }
