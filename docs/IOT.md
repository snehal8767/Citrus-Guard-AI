# IoT (Sensors)

## Current state: simulated feed, real storage

Each scan writes one `SensorReading` per zone: soil moisture (%), temperature (°C), humidity (%), leaf wetness (%), irrigation status (On/Off). Values are generated with a seeded RNG: healthy ranges for normal zones, and Zone B's anomaly signature (dry soil 18–24%, humidity 82–92%, leaf wetness 70–88% — the classic disease-favouring combo).

## Status classification

A reading is Normal / Warning / Critical by counting out-of-range metrics against agronomy-plausible bands (soil 25–45%, temp 20–35°C, humidity 40–75%, wetness ≤40%). The Sensors page shows value + normal range + status + trend + last-updated per zone.

## How real hardware plugs in

Replace the RNG block in `scan_service.run_scan` with a poll of the sensor gateway (e.g. MQTT → REST bridge writing to `POST /sensors`-style ingestion). Schema and UI need no changes: `SensorReading` already stores exactly what a field node sends. Sensor health KPI (`/metrics`) then becomes a genuine fleet-health signal.
