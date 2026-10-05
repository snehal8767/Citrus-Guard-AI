# Interview Pack

## Problem solved

Late, blanket, unrecorded crop-stress response on large Vidarbha orange orchards → zone-level scan→detect→alert→verify→act→record loop that treats 6.25 acres instead of 50.

## Key features (say 5)

1. One-transaction orchard scan with deterministic Zone B demo story
2. Real OpenCV + scikit-learn image pipeline behind a swappable `Predictor` protocol
3. Transparent risk engine with per-factor breakdown
4. Server-enforced human-in-the-loop (Verified-gated interventions, tested 400s)
5. GIS map, sensor network, command console, history, downloadable reports

## Why each technology

- **React+TS+Vite:** type-safe contracts with the API; fast builds (verified).
- **Tailwind:** design system without CSS files.
- **Recharts:** declarative charts over real history rows.
- **Leaflet+OSM:** free maps, no keys.
- **FastAPI+Pydantic:** validation + Swagger for free.
- **SQLAlchemy+SQLite+Alembic:** relational integrity with zero ops.
- **sklearn+OpenCV:** explainable classical ML; honest about being synthetic.
- **JWT+bcrypt:** auth without an identity provider.
- **pytest+Vitest:** 77 tests, all green.

## Architecture (30 seconds)

SPA → typed client → 12 FastAPI routers → service layer (scan/alerts/metrics/commands/reports) → SQLAlchemy → SQLite; AI package hangs off services via a protocol. Request path for a scan: JWT check → Pydantic validation → single DB transaction writing scan, detections, sensors, zone updates, alert, history → refresh.

## Database explanation

10 tables; zones/detections/sensors/alerts/verifications/interventions/history around one orchard. CHECKs bound scores 0–100; FK cascades with SQLite pragma on; alert transitions are a server-side state machine, not just a column.

## AI/ML explanation

128px resize → HSV/LAB/gray → 10 explainable features (greenness, lesion proxy, texture…) → 120-tree RF trained on synthetic centroids (~0.85 hold-out) → confidence → severity → weighted risk (0.30/0.20/0.20/0.15/0.15) → band → recommendation. Demo scan pins Zone B; uploads use the real path.

## Important APIs

`POST /scans` (the transaction), `POST /ai/analyze` (content-sniffed upload), `POST /alerts/{id}/verify|reject|rescan` (state machine), `POST /interventions` (Verified gate), `POST /commands` (rule parser), `GET /metrics`, `GET /reports`.

## Challenges solved

- NumPy 1.26 has no Python-3.13 wheels → pinned 2.1.3.
- `imghdr` removed in 3.13 → Pillow content-sniffing.
- SQLite FKs off by default → connect-time PRAGMA.
- CHECKs fire at flush, not commit → fixed test structure.
- jsdom lacks `createObjectURL`, Leaflet needs DOM → setup stub + module stub.
- Duplicate KPI text broke `getByText` → `getAllByText` + component text fix.

## Scalability

Stateless API (scale horizontally), SQLite→Postgres via URL, tiles/CDN for frontend, model file → model server later. Current bottlenecks: single DB file, sync scan transaction (fine at demo scale).

## Security

Bcrypt hashes, JWT expiry, Bearer on all but login/health, upload type+size validation, secrets in `.env` (never committed), no dosage content. Gaps to name: 2 roles only, no rate limiting, SQLite file permissions.

## 8 resume bullets

- Built full-stack AI orchard monitor: React+TS frontend, FastAPI service layer, SQLite — every UI number live from DB.
- Implemented classical-ML vision pipeline (OpenCV→10 features→RandomForest) behind a swappable Predictor protocol.
- Designed transparent risk engine (weighted 0–100 + factor breakdown) with banded health states.
- Enforced human-in-the-loop: server-side alert state machine; interventions require Verified alerts (400-tested).
- Shipped Leaflet GIS with 8 health-coloured zones, sensor fusion, and per-zone detail panels.
- Wrote 77 tests (pytest 57, Vitest 20) + CI; deterministic seeded demo reproducible after reset.
- Built rule-based command console mapping text to real services (explicitly not an LLM).
- Documented honestly: REAL-vs-SIMULATED matrix, validation roadmap, no accuracy claims.

## Likely questions + answers

- "Is the model accurate?" → Honest: synthetic demo (~0.85 on synthetic hold-out, meaningless in-field); interface ready for a real model; verification decisions are stored as future labels.
- "Why not a CNN?" → No labelled field data; classical features are explainable and run anywhere; protocol allows upgrade.
- "How do you prevent autonomous spraying?" → No code path exists; 400-gate tested; state machine audited.
- "Scale to 1000 farms?" → Postgres, stateless API replicas, per-farm isolation, model service; current design migrates cleanly.
- "Biggest tradeoff?" → Deterministic demo values vs ML realism; chose repeatability for judging, kept the real pipeline for uploads.

## 2-minute explanation

"Vidarbha's orange farmers walk fifty acres to spot disease, then spray everything. I built CitrusGuardAI to close that loop per zone: a scan transaction that detects stress, scores risk transparently, and raises an alert; the farmer verifies on their phone; only then can a precision plan target the six affected acres instead of fifty. The stack is React and FastAPI with SQLite, an OpenCV plus scikit-learn pipeline behind a swappable interface, Leaflet maps, and a rule-based command console. Everything is tested — fifty-seven backend and twenty frontend tests — and the demo resets deterministically. I'm explicit about limits: synthetic model, simulated drone, prototype risk formula, no dosage advice. The architecture is ready for the real thing: field data retrains the model through the same interface, sensors replace the simulator, and verification taps become training labels."
