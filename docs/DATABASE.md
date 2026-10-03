# Database

## Engine

SQLite (`backend/data/citrusguard.db`, path from `DATABASE_URL` in `.env`). Foreign-key enforcement is turned on explicitly (`PRAGMA foreign_keys=ON` in `engine.py`) so `ondelete="CASCADE"` works. Zero-ops, file-backed — ideal for a demo; swap `DATABASE_URL` for Postgres in production.

## Tables

| Table | Purpose | Key fields |
|---|---|---|
| orchards | Estate record | name, location, area (ac), crop |
| orchard_zones | 8 zones A–H | orchard FK, zone_name, area, lat/lon, health_status, risk_score |
| scans | One row per mission | orchard FK, scan_type, coverage %, status |
| ai_detections | Per-zone AI output | scan FK, zone FK, condition, confidence, severity, explanation |
| sensor_readings | IoT snapshots | zone FK, soil_moisture, temperature, humidity, leaf_wetness, irrigation_status |
| alerts | Risk alerts | zone FK, alert_type, severity, risk_score, message, status |
| farmer_verifications | Human decisions | alert FK, decision (verify/reject/rescan), comment |
| interventions | Precision plans | zone FK, type, target_area, status, reason |
| historical_monitoring | Trend source | orchard/zone/scan FKs, health_score, risk_score, affected_area |
| users | Login | username (unique), password_hash, role |

## Integrity rules

- `CHECK (risk_score BETWEEN 0 AND 100)` on zones and alerts.
- `CHECK (confidence BETWEEN 0 AND 100)` and severity limited to Low/Medium/High/Critical on detections.
- Alert status transitions enforced in `alert_service.VALID_TRANSITIONS` (server-side, tested).
- Indexes on all FKs + timestamps.

## Migrations

Alembic, single initial revision `0001`. Apply with `alembic upgrade head` from `backend/`.

## How to inspect in VS Code

1. Install **SQLite Viewer** (publisher: qwtel).
2. Open `backend/data/citrusguard.db` in the Explorer.
3. Browse the tables above. Alternative: DB Browser for SQLite.
