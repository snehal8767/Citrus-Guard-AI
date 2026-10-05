"""Build a PERSISTENT snapshot of the test database for demos/recruiters.

Run from anywhere:
    backend\\.venv\\Scripts\\python.exe backend\\snapshot_test_db.py

Then open backend\\data\\test_citrusguard.db in SQLite Viewer: tables stay
visible with demo test data (users, orchard, 8 zones, 1 scan, Zone B
detection + alert, 1 verification, 1 intervention).

NOTE: a real `pytest` run still wipes/recreates this file (test isolation).
Re-run this script afterwards to restore the snapshot.
"""
import os
import sys

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BACKEND_DIR)

TEST_DB = os.path.join(BACKEND_DIR, "data", "test_citrusguard.db")
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["UPLOAD_DIR"] = os.path.join(BACKEND_DIR, "data", "uploads")

from app.core.security import hash_password  # noqa: E402
from app.database.engine import Base, SessionLocal, engine  # noqa: E402
from app.models import Orchard, OrchardZone, User  # noqa: E402
from app.services import alert_service, scan_service  # noqa: E402

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()
db.add_all(
    [
        User(username="farmer", password_hash=hash_password("farmer123"),
             role="farmer", full_name="Test Farmer"),
        User(username="operator", password_hash=hash_password("operator123"),
             role="operator", full_name="Test Operator"),
    ]
)
orchard = Orchard(name="Test Orchard", location="Vidarbha", area=50.0,
                  crop="Orange (Nagpur Santra)")
db.add(orchard)
db.flush()
for i, name in enumerate(["A", "B", "C", "D", "E", "F", "G", "H"]):
    db.add(OrchardZone(orchard_id=orchard.id, zone_name=name, area=6.25,
                       latitude=21.14 + i * 0.001, longitude=79.08 + i * 0.001,
                       health_status="Healthy", risk_score=10.0))
db.commit()

scan = scan_service.run_scan(db, orchard.id)          # Zone B flagged
db.commit()
alert = [a for a in db.query(alert_service.Alert).all() if a.zone_id == 2][-1]
alert_service.record_verification(db, alert.id, "verify", "snapshot demo")
zone_b = db.query(OrchardZone).filter_by(zone_name="B").one()
alert_service.create_intervention(db, zone_b.id, "Targeted canopy inspection",
                                  zone_b.area, reason="snapshot demo")
db.commit()

from sqlalchemy import func  # noqa: E402
from app.models import AIDetection, Alert, FarmerVerification, Intervention, Scan  # noqa: E402
print("TEST DB snapshot ready:", TEST_DB)
print("  users:", db.query(func.count(User.id)).scalar())
print("  zones:", db.query(func.count(OrchardZone.id)).scalar())
print("  scans:", db.query(func.count(Scan.id)).scalar())
print("  detections:", db.query(func.count(AIDetection.id)).scalar())
print("  alerts:", db.query(func.count(Alert.id)).scalar())
print("  verifications:", db.query(func.count(FarmerVerification.id)).scalar())
print("  interventions:", db.query(func.count(Intervention.id)).scalar())
db.close()
