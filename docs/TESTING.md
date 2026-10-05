# Testing

## Backend — pytest (57 tests, all passing)

Run from the project root: `backend\.venv\Scripts\python.exe -m pytest tests -q`

| File | What it covers |
|---|---|
| test_health.py | /health shape, root endpoint |
| test_auth.py | Both demo logins, wrong password, 401 without token |
| test_database.py | Seed counts, relationships, CHECK constraints, cascade delete, sensor fields |
| test_risk.py | Determinism, weight math, band boundaries, severity mapping |
| test_ai_service.py | Preprocess views, garbage rejection, feature shape, full analysis fields |
| test_scan_flow.py | Zone B 91%/High, alert risk 82, zone update, history rows, 404 orchard |
| test_alerts.py | verify/reject/rescan transitions, invalid transition 400, intervention gate |
| test_commands.py | help/unknown/risk/zones/run-scan intents, metrics, report, bad upload, orchard CRUD |

Tests use an isolated SQLite file (`backend/data/test_citrusguard.db`) with per-test wipe + reseed. Notable bugs caught: CHECK firing at flush, SQLite FK pragma off, severity-95 vs 100 max-risk math.

## Frontend — Vitest + React Testing Library (20 tests, all passing)

Run from `frontend/`: `npm test`. Plus `npm run build` (tsc + vite) verified clean.

| File | What it covers |
|---|---|
| helpers.test.ts | Badge classes, zone colors, safe formatting |
| ScanProgress.test.tsx | All 12 steps + SIMULATION label |
| Dashboard.test.tsx | KPIs from API, scan button calls endpoint + refreshes, error state |
| Alerts.test.tsx | Alert list, VERIFY wiring, empty state |
| CommandConsole.test.tsx | Command round-trip, "not an LLM" label |
| ZoneMap.test.tsx | Polygons per zone, click select, popup health (react-leaflet stubbed) |
| AIAnalysis.test.tsx | Upload → analyze → results, backend error display |

jsdom gaps handled in `setupTests.ts` (`URL.createObjectURL` stub) and by stubbing `react-leaflet` (needs a real browser).
