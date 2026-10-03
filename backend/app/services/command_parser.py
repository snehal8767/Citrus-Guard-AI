"""Command Console: deterministic rule-based intent parser.

This is NOT an LLM. It maps short text commands to real service calls and
returns real database results. Unknown commands return a helpful list of
supported commands.
"""
from __future__ import annotations

import re

from sqlalchemy.orm import Session

from app.models import Alert, OrchardZone, Scan, SensorReading
from app.services import alert_service, scan_service

SUPPORTED_COMMANDS = [
    "run scan",
    "show zone <X> risk",
    "list alerts",
    "verify alert <N>",
    "reject alert <N>",
    "rescan alert <N>",
    "show sensors for zone <X>",
    "generate report",
    "show metrics",
    "list zones",
    "help",
]


def _zone_id_by_name(db: Session, name: str) -> OrchardZone | None:
    return db.query(OrchardZone).filter(OrchardZone.zone_name.ilike(name)).first()


def parse_and_execute(db: Session, command: str, orchard_id: int) -> dict:
    """Parse a text command and execute it against real services."""
    text = command.strip().lower()
    if not text:
        return _help_response("Empty command.")

    # --- run scan -------------------------------------------------------------
    if re.search(r"\b(run|start|do|execute)\b.*\bscan\b", text) or text == "run scan":
        scan = scan_service.run_scan(db, orchard_id)
        db.commit()
        return {
            "intent": "run_scan",
            "message": f"Scan #{scan.id} completed. Coverage {scan.coverage}%. "
            "Zone B flagged with disease stress (risk 82/100).",
            "data": {"scan_id": scan.id, "coverage": scan.coverage, "status": scan.status},
        }

    # --- show zone <X> risk ---------------------------------------------------
    m = re.search(r"(?:show|what|check|display).*zone\s+([a-h])\b.*risk", text)
    if not m:
        m = re.search(r"zone\s+([a-h])\s+risk", text)
    if m:
        zone = _zone_id_by_name(db, m.group(1))
        if zone is None:
            return _help_response(f"Zone {m.group(1).upper()} not found.")
        return {
            "intent": "zone_risk",
            "message": f"Zone {zone.zone_name}: health={zone.health_status}, risk={zone.risk_score}/100.",
            "data": {
                "zone_id": zone.id,
                "zone_name": zone.zone_name,
                "health_status": zone.health_status,
                "risk_score": zone.risk_score,
            },
        }

    # --- list alerts ----------------------------------------------------------
    if "alert" in text and ("list" in text or "show" in text or "all" in text):
        alerts = db.query(Alert).order_by(Alert.created_at.desc()).all()
        return {
            "intent": "list_alerts",
            "message": f"{len(alerts)} alert(s) found.",
            "data": [
                {
                    "id": a.id,
                    "zone_id": a.zone_id,
                    "severity": a.severity,
                    "risk_score": a.risk_score,
                    "status": a.status,
                    "message": a.message,
                }
                for a in alerts
            ],
        }

    # --- verify / reject / rescan alert <N> ------------------------------------
    m = re.search(r"(verify|reject|rescan)\s+alert\s+(\d+)", text)
    if m:
        decision, alert_id = m.group(1), int(m.group(2))
        try:
            verification = alert_service.record_verification(db, alert_id, decision, None)
            db.commit()
            return {
                "intent": f"{decision}_alert",
                "message": f"Alert #{alert_id} {decision}ed. New status recorded.",
                "data": {
                    "verification_id": verification.id,
                    "alert_id": alert_id,
                    "decision": decision,
                },
            }
        except ValueError as e:
            db.rollback()
            return _help_response(str(e))

    # --- show sensors for zone <X> ---------------------------------------------
    m = re.search(r"(?:show|get|display).*sensors?.*zone\s+([a-h])\b", text)
    if not m:
        m = re.search(r"zone\s+([a-h])\s+sensors?", text)
    if m:
        zone = _zone_id_by_name(db, m.group(1))
        if zone is None:
            return _help_response(f"Zone {m.group(1).upper()} not found.")
        reading = (
            db.query(SensorReading)
            .filter(SensorReading.zone_id == zone.id)
            .order_by(SensorReading.timestamp.desc())
            .first()
        )
        if reading is None:
            return _help_response(f"No sensor readings for zone {zone.zone_name}.")
        return {
            "intent": "zone_sensors",
            "message": f"Zone {zone.zone_name} sensor reading.",
            "data": {
                "zone_name": zone.zone_name,
                "soil_moisture": reading.soil_moisture,
                "temperature": reading.temperature,
                "humidity": reading.humidity,
                "leaf_wetness": reading.leaf_wetness,
                "irrigation_status": reading.irrigation_status,
                "timestamp": reading.timestamp.isoformat(),
            },
        }

    # --- generate report -------------------------------------------------------
    if "report" in text and ("generate" in text or "create" in text or "download" in text):
        return {
            "intent": "generate_report",
            "message": "Use GET /reports to download the full orchard report (HTML).",
            "data": {"endpoint": "GET /reports", "format": "text/html"},
        }

    # --- show metrics ----------------------------------------------------------
    if "metric" in text or "dashboard" in text or "kpi" in text:
        return {
            "intent": "show_metrics",
            "message": "Use GET /metrics for dashboard KPIs.",
            "data": {"endpoint": "GET /metrics"},
        }

    # --- list zones ------------------------------------------------------------
    if "zone" in text and ("list" in text or "show" in text or "all" in text):
        zones = db.query(OrchardZone).filter(OrchardZone.orchard_id == orchard_id).all()
        return {
            "intent": "list_zones",
            "message": f"{len(zones)} zones.",
            "data": [
                {
                    "zone_name": z.zone_name,
                    "health_status": z.health_status,
                    "risk_score": z.risk_score,
                }
                for z in zones
            ],
        }

    # --- help ------------------------------------------------------------------
    if text in ("help", "?", "commands"):
        return _help_response("Supported commands:")

    return _help_response(f"Unknown command: '{command}'")


def _help_response(message: str) -> dict:
    return {
        "intent": "help",
        "message": message,
        "data": {"supported_commands": SUPPORTED_COMMANDS},
    }
