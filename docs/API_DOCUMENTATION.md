# API Documentation

Interactive docs: **http://localhost:8000/docs** (Swagger) and `/redoc`.

## Conventions

- Auth: `POST /auth/login` → Bearer JWT. All other endpoints require it (401 otherwise).
- Errors: 400 for bad input/state, 404 for missing resources, with a plain-English `detail`.
- Uploads: content-sniffed with Pillow (not extension), size-limited by `MAX_UPLOAD_MB`.

## Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | /health | no | Liveness + demo_mode flag |
| POST | /auth/login | no | Farmer/operator login → JWT |
| GET/POST | /orchards | yes | List / create (full CRUD with PUT/DELETE /{id}) |
| GET | /orchards/{id} | yes | Orchard with zones |
| GET/POST | /zones | yes | List (filter `orchard_id`) / create (full CRUD with PUT/DELETE /{id}) |
| GET/POST | /scans | yes | List / run full scan transaction |
| GET | /scans/{id} | yes | Scan with detections |
| POST | /ai/analyze | yes | Image upload → condition/confidence/severity/explanation/next step (recorded in DB) |
| GET | /ai/analyses | yes | Past upload analyses, newest first |
| GET | /sensors | yes | Readings (filter `zone_id`, `limit`) |
| GET | /sensors/status | yes | Latest per-zone + Normal/Warning/Critical |
| GET | /alerts | yes | List (filter `status`) |
| GET | /alerts/{id} | yes | Single alert |
| POST | /alerts/{id}/verify | yes | verify decision → Verified |
| POST | /alerts/{id}/reject | yes | reject decision → Rejected |
| POST | /alerts/{id}/rescan | yes | rescan decision → Rescan Requested |
| GET/POST | /interventions | yes | List / create (requires Verified alert, else 400) |
| GET | /history | yes | Monitoring records (filter orchard/zone) |
| GET | /metrics | yes | Dashboard KPIs |
| GET | /reports | yes | Downloadable HTML report |
| POST | /commands | yes | Rule-based text commands (NOT an LLM) |

## Alert state machine

New → {Under Review, Verified, Rejected, Rescan Requested}; Under Review → {Verified, Rejected, Rescan Requested}; Verified → {Action Planned, Resolved}; Rejected → {Rescan Requested}; Rescan Requested → {New, Under Review}; Action Planned → {Resolved}. Anything else → 400 "Invalid transition".

See README for curl examples.
