# Drone Workflow

## Status: SIMULATION (labelled everywhere in UI and docs)

No real drone is controlled. The Drone Mission page animates battery, coverage, and images-captured telemetry while the real `POST /scans` call executes.

## The 12 animated steps

Initializing drone mission → Scanning orchard → Collecting imagery → Processing imagery → Running AI analysis → Checking sensor data → Detecting crop-health anomaly → Calculating risk → Updating GIS map → Generating alert → Waiting for farmer verification → Generating intervention plan.

Each maps to a real backend stage; the last two map to the human-in-the-loop workflow (alert state + intervention planning), which is why "waiting for farmer verification" is a step: the mission is not complete until a human confirms.

## Mission history

Every mission persists as a `Scan` row (type `drone_simulation`, coverage %, status). The page lists them from the database — re-running the demo appends real rows.

## Future field deployment

Swap the animation driver for a mission API (e.g. DJI/ArduPilot waypoint upload + telemetry webhook). The `Scan` model already has `scan_type`/`coverage`/`status` fields to record real flights; imagery would land in `data/images/` and flow into `POST /ai/analyze`.
