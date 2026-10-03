# Project Overview

CitrusGuardAI is an AI-powered farm monitoring and automation system for **large orange orchards (50+ acres) in Vidarbha, Maharashtra, India** — the belt famous for Nagpur Santra (mandarin oranges).

## The demo farm

One fictional farm is seeded: **Vidarbha Orange Estate**, 50 acres near Nagpur, split into **8 zones (A–H)** of 6.25 acres each. Fourteen days of scan + sensor history ship with the seed so every chart has real data from the first login.

## What the system does

1. **Monitors** — drone-simulation scans record coverage, imagery analysis, and sensor snapshots per zone.
2. **Detects** — an OpenCV + scikit-learn pipeline classifies crop stress; the scan service deterministically flags Zone B in demo mode (91% confidence, High severity, risk 82/100).
3. **Maps** — Leaflet GIS map colours zones by health; clicking a zone shows health, risk, AI confidence, sensors, and the recommended action.
4. **Alerts** — risk-scored alerts with a transparent per-factor breakdown.
5. **Intervenes precisely** — plans target only the affected zone (6.25 ac vs 50 ac), but **only after a farmer verifies the alert** (human-in-the-loop).
6. **Records everything** — every scan, detection, verification, and intervention lands in history; one click downloads an HTML report.

## Who it is for

- **Farmers** (farmer role): verify alerts, approve interventions, read reports.
- **Orchard operators** (operator role): run scans, monitor sensors, manage zones.
- **Hackathon judges / recruiters**: a clean, explainable, fully working full-stack + AI project.

## Honest boundaries

- Demo classifier trained on **synthetic** features — not field-validated.
- Drone is a **simulation** (animated telemetry, real backend results).
- 91% / 82/100 are **deterministic demo values**.
- Risk engine is a **prototype formula**, not agronomy.
- **No pesticide dosage anywhere** — by design.
