"""Alert service: state machine, verification, and intervention generation.

Alert states: New, Under Review, Verified, Rejected, Rescan Requested,
Action Planned, Resolved.

HUMAN-IN-THE-LOOP: an intervention can only be created after an alert is
Verified by a user. The AI never executes an intervention by itself.
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Alert, FarmerVerification, Intervention, OrchardZone

# Valid state transitions (server-enforced).
VALID_TRANSITIONS: dict[str, set[str]] = {
    "New": {"Under Review", "Verified", "Rejected", "Rescan Requested"},
    "Under Review": {"Verified", "Rejected", "Rescan Requested"},
    "Verified": {"Action Planned", "Resolved"},
    "Rejected": {"Rescan Requested"},
    "Rescan Requested": {"New", "Under Review"},
    "Action Planned": {"Resolved"},
    "Resolved": set(),
}

DECISION_TO_STATUS = {
    "verify": "Verified",
    "reject": "Rejected",
    "rescan": "Rescan Requested",
}


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def transition_alert(db: Session, alert: Alert, new_status: str) -> Alert:
    """Enforce a valid state transition. Raises ValueError on invalid moves."""
    allowed = VALID_TRANSITIONS.get(alert.status, set())
    if new_status not in allowed:
        raise ValueError(
            f"Invalid transition: {alert.status} -> {new_status}. "
            f"Allowed: {sorted(allowed) or 'none (terminal state)'}"
        )
    alert.status = new_status
    db.flush()
    return alert


def record_verification(
    db: Session, alert_id: int, decision: str, comment: str | None
) -> FarmerVerification:
    """Record a farmer verification and advance the alert state."""
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise ValueError(f"Alert {alert_id} not found")

    decision = decision.lower().strip()
    if decision not in DECISION_TO_STATUS:
        raise ValueError(f"Unknown decision '{decision}'. Use: verify, reject, rescan")

    new_status = DECISION_TO_STATUS[decision]
    transition_alert(db, alert, new_status)

    verification = FarmerVerification(
        alert_id=alert.id,
        decision=decision,
        comment=comment,
        timestamp=utcnow(),
    )
    db.add(verification)
    db.flush()
    return verification


def create_intervention(
    db: Session,
    zone_id: int,
    intervention_type: str,
    target_area: float,
    reason: str | None = None,
) -> Intervention:
    """Create a precision intervention plan. Requires a Verified alert on the zone."""
    zone = db.get(OrchardZone, zone_id)
    if zone is None:
        raise ValueError(f"Zone {zone_id} not found")

    # Human-in-the-loop guard: must have a Verified alert.
    verified = (
        db.query(Alert)
        .filter(Alert.zone_id == zone_id, Alert.status == "Verified")
        .first()
    )
    if verified is None:
        raise ValueError(
            f"Cannot create intervention for zone {zone_id}: "
            "no Verified alert. Farmer verification is required (human-in-the-loop)."
        )

    intervention = Intervention(
        zone_id=zone_id,
        intervention_type=intervention_type,
        target_area=target_area,
        status="Planned",
        reason=reason or f"Based on verified alert #{verified.id} (risk {verified.risk_score:.0f}/100).",
    )
    db.add(intervention)

    # Advance the alert to Action Planned.
    transition_alert(db, verified, "Action Planned")

    db.flush()
    return intervention
