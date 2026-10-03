# FAQ

**Is the disease detection real?**
No. The classifier trains on synthetic features and the scan returns fixed demo values for Zone B. Real uploads do run the genuine OpenCV→features→RandomForest pipeline, but treat labels as demo output.

**Does it control a drone?**
No. The mission page is an animated simulation; results come from the backend scan transaction.

**Why deterministic Zone B?**
Repeatability. Judges and recruiters see the same story every reset. Randomness would make the demo unrehearsable.

**Can the AI spray or act alone?**
No — architecturally. `POST /interventions` returns 400 without a Verified alert. There is no code path from detection to action that skips the farmer.

**Why no pesticide recommendations?**
Safety and scope. Dosage depends on product, pest, weather, and regulation — a demo must not guess. Intervention types are actions (inspect, irrigate, prune, monitor).

**SQLite for a real farm?**
For one farm's demo, yes. Multi-farm production wants Postgres — the SQLAlchemy layer makes that a config change.

**How do I plug in a real model?**
Implement the `Predictor` protocol (`predict(features) -> {condition, confidence}`) and return it from `get_predictor()`. Nothing else changes.

**How do real sensors plug in?**
Replace the RNG block in `scan_service.run_scan` with gateway reads. The `SensorReading` schema already matches field-node payloads.

**What does it cost to run?**
₹0 in software. See COST_ANALYSIS.md for hardware estimates.
