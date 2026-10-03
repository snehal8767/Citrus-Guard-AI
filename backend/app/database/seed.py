"""Seed the database with the fictional 50-acre Vidarbha orange orchard.

Usage:
    python -m app.database.seed           # seed only if empty
    python -m app.database.seed --reset   # wipe and reseed (deterministic demo)
"""
import argparse
import json
import math
import os
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from app.core.config import get_settings
from app.core.security import hash_password
from app.database.engine import Base, SessionLocal, engine
from app.models import (
    AIDetection,
    Alert,
    FarmerVerification,
    HistoricalMonitoring,
    Intervention,
    Orchard,
    OrchardZone,
    Scan,
    SensorReading,
    User,
)

# --- Fictional orchard geometry -------------------------------------------------
# Vidarbha (Nagpur region), Maharashtra. 50 acres split into 8 zones (A-H).
ORCHARD_CENTER_LAT = 21.1458
ORCHARD_CENTER_LON = 79.0882
ORCHARD_AREA_ACRES = 50.0
ZONE_AREA_ACRES = ORCHARD_AREA_ACRES / 8.0  # 6.25 acres each

# Grid layout: 4 columns x 2 rows. ~0.0045 deg lat (~500m) per cell.
COLS = 4
ROWS = 2
LAT_STEP = 0.0045
LON_STEP = 0.0052
ZONE_NAMES = ["A", "B", "C", "D", "E", "F", "G", "H"]

# Zone B is the deterministic demo anomaly zone.
DEMO_ZONE_NAME = "B"

# Normal sensor ranges for a healthy orange orchard in Vidarbha.
NORMAL_RANGES = {
    "soil_moisture": (28.0, 42.0),
    "temperature": (22.0, 33.0),
    "humidity": (45.0, 70.0),
    "leaf_wetness": (5.0, 30.0),
}

# Zone B anomaly signature: high leaf wetness + humidity, abnormal soil moisture.
ZONE_B_ANOMALY = {
    "soil_moisture": (18.0, 24.0),   # too dry
    "temperature": (30.0, 35.0),
    "humidity": (82.0, 92.0),        # very humid
    "leaf_wetness": (70.0, 88.0),    # prolonged leaf wetness -> disease risk
}


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def build_zone_geometry() -> list[dict]:
    """Return a list of 8 zone dicts with lat/lon center and a square polygon."""
    zones = []
    start_lat = ORCHARD_CENTER_LAT - (ROWS - 1) * LAT_STEP / 2
    start_lon = ORCHARD_CENTER_LON - (COLS - 1) * LON_STEP / 2
    for idx, name in enumerate(ZONE_NAMES):
        row = idx // COLS
        col = idx % COLS
        lat = start_lat + row * LAT_STEP
        lon = start_lon + col * LON_STEP
        dlat = LAT_STEP / 2 * 0.9
        dlon = LON_STEP / 2 * 0.9
        polygon = {
            "type": "Polygon",
            "coordinates": [
                [
                    [lon - dlon, lat - dlat],
                    [lon + dlon, lat - dlat],
                    [lon + dlon, lat + dlat],
                    [lon - dlon, lat + dlat],
                    [lon - dlon, lat - dlat],
                ]
            ],
        }
        zones.append(
            {
                "zone_name": name,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "area": ZONE_AREA_ACRES,
                "polygon": polygon,
            }
        )
    return zones


def write_geojson(zones: list[dict]) -> None:
    """Write the orchard boundary + zones to data/geojson for the frontend map."""
    settings = get_settings()
    geo_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "geojson")
    os.makedirs(geo_dir, exist_ok=True)

    # Individual zone files
    for z in zones:
        path = os.path.join(geo_dir, f"zone_{z['zone_name']}.geojson")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "type": "Feature",
                    "properties": {
                        "zone_name": z["zone_name"],
                        "orchard": "Vidarbha Orange Estate",
                        "area_acres": z["area"],
                    },
                    "geometry": z["polygon"],
                },
                f,
                indent=2,
            )

    # Combined orchard boundary file
    all_coords = []
    for z in zones:
        all_coords.extend(z["polygon"]["coordinates"][0][:-1])
    # Convex-ish boundary: just use the outer ring of all zone corners
    boundary = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Vidarbha Orange Estate", "area_acres": ORCHARD_AREA_ACRES},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [min(c[0] for c in all_coords), min(c[1] for c in all_coords)],
                            [max(c[0] for c in all_coords), min(c[1] for c in all_coords)],
                            [max(c[0] for c in all_coords), max(c[1] for c in all_coords)],
                            [min(c[0] for c in all_coords), max(c[1] for c in all_coords)],
                            [min(c[0] for c in all_coords), min(c[1] for c in all_coords)],
                        ]
                    ],
                },
            }
        ],
    }
    with open(os.path.join(geo_dir, "orchard_boundary.geojson"), "w", encoding="utf-8") as f:
        json.dump(boundary, f, indent=2)


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _sample_sensor(zone_name: str, rng: random.Random, day_offset: int) -> dict:
    """Sample a sensor reading. Zone B carries the anomaly signature."""
    if zone_name == DEMO_ZONE_NAME:
        ranges = ZONE_B_ANOMALY
        irrigation = "Off"
    else:
        ranges = NORMAL_RANGES
        irrigation = "On" if rng.random() < 0.3 else "Off"
    return {
        "soil_moisture": round(rng.uniform(*ranges["soil_moisture"]), 1),
        "temperature": round(rng.uniform(*ranges["temperature"]), 1),
        "humidity": round(rng.uniform(*ranges["humidity"]), 1),
        "leaf_wetness": round(rng.uniform(*ranges["leaf_wetness"]), 1),
        "irrigation_status": irrigation,
    }


def seed(reset: bool = False) -> None:
    Base.metadata.create_all(bind=engine)
    write_geojson(build_zone_geometry())

    db = SessionLocal()
    try:
        existing = db.scalar(select(func.count()).select_from(Orchard))
        if existing and not reset:
            print("[seed] Database already seeded. Use --reset to reseed.")
            return
        if reset:
            print("[reset] Clearing existing data...")
            for table in reversed(Base.metadata.sorted_tables):
                db.execute(table.delete())
            db.commit()

        now = utcnow()
        rng = random.Random(42)  # deterministic demo data

        # --- Users -------------------------------------------------------------
        farmer = User(
            username="farmer",
            password_hash=hash_password("farmer123"),
            role="farmer",
            full_name="Ramesh Deshmukh",
        )
        operator = User(
            username="operator",
            password_hash=hash_password("operator123"),
            role="operator",
            full_name="Priya Kulkarni",
        )
        db.add_all([farmer, operator])

        # --- Orchard + zones ---------------------------------------------------
        orchard = Orchard(
            name="Vidarbha Orange Estate",
            location="Nagpur, Vidarbha, Maharashtra, India",
            area=ORCHARD_AREA_ACRES,
            crop="Orange (Nagpur Santra)",
            created_at=now - timedelta(days=90),
        )
        db.add(orchard)
        db.flush()

        zones: dict[str, OrchardZone] = {}
        for z in build_zone_geometry():
            zone = OrchardZone(
                orchard_id=orchard.id,
                zone_name=z["zone_name"],
                area=z["area"],
                latitude=z["latitude"],
                longitude=z["longitude"],
                health_status="At Risk" if z["zone_name"] == DEMO_ZONE_NAME else "Healthy",
                risk_score=82.0 if z["zone_name"] == DEMO_ZONE_NAME else round(rng.uniform(5, 25), 1),
            )
            db.add(zone)
            zones[z["zone_name"]] = zone
        db.flush()

        # --- Historical scans + detections + sensors (past 14 days) -------------
        for day in range(14, 0, -1):
            scan_time = now - timedelta(days=day, hours=6)
            scan = Scan(
                orchard_id=orchard.id,
                scan_type="drone_simulation",
                timestamp=scan_time,
                coverage=round(rng.uniform(92, 100), 1),
                status="Completed",
            )
            db.add(scan)
            db.flush()

            for name, zone in zones.items():
                reading = _sample_sensor(name, rng, day)
                db.add(
                    SensorReading(
                        zone_id=zone.id,
                        timestamp=scan_time + timedelta(minutes=rng.randint(0, 30)),
                        **reading,
                    )
                )

                if name == DEMO_ZONE_NAME:
                    condition = "Possible Citrus Disease Stress"
                    confidence = round(rng.uniform(88, 93), 1)
                    severity = "High"
                    risk = round(rng.uniform(78, 86), 1)
                    health = round(rng.uniform(35, 48), 1)
                    affected = round(ZONE_AREA_ACRES * rng.uniform(0.4, 0.7), 2)
                else:
                    condition = "Healthy"
                    confidence = round(rng.uniform(90, 98), 1)
                    severity = "Low"
                    risk = round(rng.uniform(4, 22), 1)
                    health = round(rng.uniform(82, 96), 1)
                    affected = 0.0

                db.add(
                    AIDetection(
                        scan_id=scan.id,
                        zone_id=zone.id,
                        condition=condition,
                        confidence=confidence,
                        severity=severity,
                        explanation=(
                            "Elevated leaf wetness and humidity with low soil moisture "
                            "indicate favourable conditions for citrus disease development."
                            if name == DEMO_ZONE_NAME
                            else "Canopy colour, texture and sensor readings within normal range."
                        ),
                        timestamp=scan_time,
                    )
                )
                db.add(
                    HistoricalMonitoring(
                        orchard_id=orchard.id,
                        zone_id=zone.id,
                        scan_id=scan.id,
                        health_score=health,
                        risk_score=risk,
                        affected_area=affected,
                        recorded_at=scan_time,
                    )
                )

        # --- One open demo alert on Zone B (from the most recent historical scan)
        last_scan = db.scalar(
            select(Scan).where(Scan.orchard_id == orchard.id).order_by(Scan.timestamp.desc())
        )
        zone_b = zones[DEMO_ZONE_NAME]
        demo_alert = Alert(
            zone_id=zone_b.id,
            alert_type="Disease Risk",
            severity="High",
            risk_score=82.0,
            message=(
                "Zone B: Possible Citrus Disease Stress detected (confidence 91%, risk 82/100). "
                "High leaf wetness and humidity with abnormal soil moisture. "
                "Farmer verification required before any intervention."
            ),
            status="New",
            created_at=now - timedelta(hours=2),
        )
        db.add(demo_alert)

        db.commit()
        print("[seed] Done.")
        print(f"  Orchard : {orchard.name} ({orchard.area} acres, 8 zones A-H)")
        print(f"  Users   : farmer/farmer123 (farmer), operator/operator123 (operator)")
        print(f"  Demo    : Zone B flagged with disease stress, risk 82/100")
        print(f"  History : 14 days of scans, detections and sensor readings")
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed CitrusGuardAI demo database")
    parser.add_argument("--reset", action="store_true", help="wipe and reseed")
    args = parser.parse_args()
    seed(reset=args.reset)


if __name__ == "__main__":
    main()
