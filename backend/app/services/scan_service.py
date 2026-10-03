"""Scan service: orchestrates the full orchard scan flow in one DB transaction.

Flow: create scan -> simulate coverage per zone -> run AI -> read sensors ->
compute risk -> update zone health -> write AIDetection -> create Alert ->
append HistoricalMonitoring.
"""
from __future__ import annotations

import random
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.ai.risk import risk_band
from app.models import (
    AIDetection,
    Alert,
    HistoricalMonitoring,
    Orchard,
    OrchardZone,
    Scan,
    SensorReading,
)

# Deterministic demo values for the official orchard scan (Zone B).
DEMO_ZONE_NAME = "B"
DEMO_CONDITION = "Possible Citrus Disease Stress"
DEMO_CONFIDENCE = 91.0
DEMO_SEVERITY = "High"
DEMO_RISK = 82.0
DEMO_RECOMMENDATION = "Verify affected trees before intervention."

# Sensor anomaly signature for Zone B (matches the seed data).
DEMO_SENSOR_ANOMALY = 85.0
DEMO_ENV_STRESS = 70.0
DEMO_HISTORY_FREQ = 80.0


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def run_scan(db: Session, orchard_id: int, scan_type: str = "drone_simulation") -> Scan:
    """Execute the full scan flow. Commits on success, rolls back on error."""
    orchard = db.get(Orchard, orchard_id)
    if orchard is None:
        raise ValueError(f"Orchard {orchard_id} not found")

    zones = db.query(OrchardZone).filter(OrchardZone.orchard_id == orchard_id).all()
    if not zones:
        raise ValueError(f"Orchard {orchard_id} has no zones")

    now = utcnow()
    rng = random.Random()

    scan = Scan(
        orchard_id=orchard_id,
        scan_type=scan_type,
        timestamp=now,
        coverage=round(rng.uniform(95, 100), 1),
        status="Completed",
    )
    db.add(scan)
    db.flush()

    alerts_created: list[Alert] = []

    for zone in zones:
        is_demo_zone = zone.zone_name == DEMO_ZONE_NAME

        # --- Sensor reading (deterministic anomaly for demo zone) ------------
        if is_demo_zone:
            reading = SensorReading(
                zone_id=zone.id,
                soil_moisture=round(rng.uniform(18, 24), 1),
                temperature=round(rng.uniform(30, 35), 1),
                humidity=round(rng.uniform(82, 92), 1),
                leaf_wetness=round(rng.uniform(70, 88), 1),
                irrigation_status="Off",
                timestamp=now,
            )
            sensor_anomaly = DEMO_SENSOR_ANOMALY
            env_stress = DEMO_ENV_STRESS
            history_freq = DEMO_HISTORY_FREQ
        else:
            reading = SensorReading(
                zone_id=zone.id,
                soil_moisture=round(rng.uniform(28, 42), 1),
                temperature=round(rng.uniform(22, 33), 1),
                humidity=round(rng.uniform(45, 70), 1),
                leaf_wetness=round(rng.uniform(5, 30), 1),
                irrigation_status="On" if rng.random() < 0.3 else "Off",
                timestamp=now,
            )
            sensor_anomaly = round(rng.uniform(5, 20), 1)
            env_stress = round(rng.uniform(5, 25), 1)
            history_freq = round(rng.uniform(0, 15), 1)
        db.add(reading)

        # --- AI detection (deterministic for demo zone) ----------------------
        if is_demo_zone:
            condition = DEMO_CONDITION
            confidence = DEMO_CONFIDENCE
            severity = DEMO_SEVERITY
            risk_score = DEMO_RISK
            explanation = (
                "Elevated leaf wetness and humidity with abnormal soil moisture "
                "indicate favourable conditions for citrus disease development."
            )
        else:
            condition = "Healthy"
            confidence = round(rng.uniform(90, 98), 1)
            severity = "Low"
            risk_score = round(rng.uniform(4, 22), 1)
            explanation = "Canopy colour, texture and sensor readings within normal range."

        detection = AIDetection(
            scan_id=scan.id,
            zone_id=zone.id,
            condition=condition,
            confidence=confidence,
            severity=severity,
            explanation=explanation,
            timestamp=now,
        )
        db.add(detection)

        # --- Update zone health ---------------------------------------------
        band = risk_band(risk_score)
        zone.health_status = band
        zone.risk_score = risk_score

        # --- Historical monitoring record -----------------------------------
        affected = round(zone.area * rng.uniform(0.4, 0.7), 2) if is_demo_zone else 0.0
        health = round(100 - risk_score, 1)
        db.add(
            HistoricalMonitoring(
                orchard_id=orchard_id,
                zone_id=zone.id,
                scan_id=scan.id,
                health_score=health,
                risk_score=risk_score,
                affected_area=affected,
                recorded_at=now,
            )
        )

        # --- Create alert for the demo zone ---------------------------------
        if is_demo_zone:
            alert = Alert(
                zone_id=zone.id,
                alert_type="Disease Risk",
                severity=severity,
                risk_score=risk_score,
                message=(
                    f"Zone {zone.zone_name}: {condition} detected "
                    f"(confidence {confidence:.0f}%, risk {risk_score:.0f}/100). "
                    f"High leaf wetness and humidity with abnormal soil moisture. "
                    f"Farmer verification required before any intervention."
                ),
                status="New",
                created_at=now,
            )
            db.add(alert)
            alerts_created.append(alert)

    db.flush()
    db.refresh(scan)
    return scan
