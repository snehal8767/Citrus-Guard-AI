"""Database tests: relationships, constraints, row counts."""
import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.models import AIDetection, Alert, Orchard, OrchardZone, Scan, SensorReading, User


def test_tables_seeded(db):
    assert db.scalar(select(func.count()).select_from(User)) == 2
    assert db.scalar(select(func.count()).select_from(Orchard)) == 1
    assert db.scalar(select(func.count()).select_from(OrchardZone)) == 8


def test_zone_belongs_to_orchard(db):
    zone = db.query(OrchardZone).filter_by(zone_name="B").one()
    assert zone.orchard.name == "Test Orchard"
    assert len(zone.orchard.zones) == 8


def test_risk_score_check_constraint(db):
    zone = db.query(OrchardZone).first()
    zone.risk_score = 150.0
    with pytest.raises(IntegrityError):
        db.flush()
    db.rollback()


def test_confidence_check_constraint(db):
    scan = Scan(orchard_id=1, scan_type="t", coverage=100.0, status="Completed")
    db.add(scan)
    db.flush()
    db.add(
        AIDetection(scan_id=scan.id, zone_id=1, condition="Healthy",
                    confidence=120.0, severity="Low")
    )
    with pytest.raises(IntegrityError):
        db.flush()
    db.rollback()


def test_severity_check_constraint(db):
    scan = Scan(orchard_id=1, scan_type="t", coverage=100.0, status="Completed")
    db.add(scan)
    db.flush()
    db.add(
        AIDetection(scan_id=scan.id, zone_id=1, condition="Healthy",
                    confidence=90.0, severity="Extreme")
    )
    with pytest.raises(IntegrityError):
        db.flush()
    db.rollback()


def test_alert_cascade_zone(db):
    zone = db.query(OrchardZone).first()
    db.add(Alert(zone_id=zone.id, alert_type="T", severity="High",
                 risk_score=80.0, message="m", status="New"))
    db.commit()
    assert db.query(Alert).count() == 1
    db.delete(zone)
    db.commit()
    assert db.query(Alert).count() == 0


def test_sensor_reading_fields(db):
    zone = db.query(OrchardZone).first()
    db.add(SensorReading(zone_id=zone.id, soil_moisture=30.0, temperature=28.0,
                         humidity=60.0, leaf_wetness=20.0, irrigation_status="Off"))
    db.commit()
    reading = db.query(SensorReading).one()
    assert reading.temperature == 28.0
    assert reading.timestamp is not None
