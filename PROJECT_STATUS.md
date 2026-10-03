# CitrusGuardAI — Project Status

_Last updated: Phase 1 complete_

## What this is
AI-powered farm monitoring and automation for large orange orchards in Vidarbha, Maharashtra.
Full-stack: React + TypeScript + Vite + Tailwind frontend, FastAPI + SQLAlchemy + SQLite backend,
scikit-learn AI module, JWT auth, human-in-the-loop alert verification.

## Tech stack
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Recharts, Leaflet + OpenStreetMap, React Router
- **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.x, SQLite, Alembic, python-jose JWT
- **AI/ML:** NumPy, Pandas, OpenCV, scikit-learn (synthetic-trained demo classifier)
- **Tests:** pytest + httpx (backend), Vitest + React Testing Library (frontend)

## Phase status
| Phase | Name | Status |
|---|---|---|
| 1 | Structure & config | ✅ Complete |
| 2 | Database, models, seed | ✅ Complete (alembic 0001 applied, seed verified) |
| 3 | AI/ML package | ✅ Complete (synthetic RF model trained, acc 0.855) |
| 4 | Backend API | ✅ Complete (full demo flow verified via API) |
| 5 | Frontend | 🟡 In progress |
| 6 | Tests | ⬜ Not started |
| 7 | Docs & polish | ⬜ Not started |

## Key design decisions
- Project root is this folder (`CitrusGuardAI`). No nested parent folder.
- SQLite at `backend/data/citrusguard.db` (path from `.env`).
- Demo mode is deterministic: official orchard scan always flags Zone B with
  confidence 91%, severity High, risk 82/100.
- Human-in-the-loop: interventions can only be created after an alert is Verified.
- No pesticide dosage anywhere. No scientifically-validated claims.

## Run commands
See `RUN_LOCAL.md` (written in Phase 7 with the exact verified commands).

## Known limitations
- AI classifier is trained on synthetic feature data (demo only).
- Drone mission is a simulation.
- Risk engine is a transparent prototype formula, not a validated agricultural model.
