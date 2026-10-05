# RUN_LOCAL — exact verified commands

These commands were actually run on Windows (PowerShell) during the build. On macOS/Linux, use the `source` + `cp` variants noted below.

## 0. Prerequisites (verified versions)

- Python 3.13.14 (`python --version`)
- Node v24.18.1, npm 11.16.0
- Git 2.55.0

> Note: `requirements.txt` pins `numpy==2.1.3` because NumPy 1.26 has no prebuilt wheel for Python 3.13.

## 1. First-time setup

```powershell
cd C:\Users\sneha\OneDrive\Desktop\CitrusGuardAI

# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy ..\.env.example .env
copy ..\.env.example ..\.env
alembic upgrade head
python -m app.database.seed
python -m app.ai.train_demo_model
```

macOS/Linux equivalents: `python3 -m venv .venv`, `source .venv/bin/activate`, `cp ../.env.example .env`.

```powershell
# Frontend (new terminal, from project root)
cd frontend
npm install
```

If PowerShell blocks venv activation: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## 2. Every run (two terminals)

Terminal 1 — backend:

```powershell
cd C:\Users\sneha\OneDrive\Desktop\CitrusGuardAI\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --port 8000
```

Terminal 2 — frontend:

```powershell
cd C:\Users\sneha\OneDrive\Desktop\CitrusGuardAI\frontend
npm run dev
```

## 3. URLs

- App: http://localhost:5173
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

Demo logins: `farmer / farmer123` · `operator / operator123`

## 4. Tests and build (all verified passing)

```powershell
# Backend: 50 tests (run from project ROOT)
cd C:\Users\sneha\OneDrive\Desktop\CitrusGuardAI
backend\.venv\Scripts\python.exe -m pytest tests -q
```

```powershell
# Frontend: 19 tests + production build
cd C:\Users\sneha\OneDrive\Desktop\CitrusGuardAI\frontend
npm test
npm run build
```

## 5. Reset the demo (deterministic reseed)

```powershell
cd C:\Users\sneha\OneDrive\Desktop\CitrusGuardAI\backend
.\.venv\Scripts\Activate.ps1
python -m app.database.seed --reset
```

## 6. Quick API checks

```powershell
Invoke-RestMethod http://localhost:8000/health
```

With curl (login first, then use the token for protected endpoints — see README for examples).

## 7. Inspect the database in VS Code

1. Install extension **SQLite Viewer** (publisher: qwtel).
2. Open `backend/data/citrusguard.db` in the Explorer.
3. Browse: orchards, orchard_zones, scans, ai_detections, sensor_readings, alerts, farmer_verifications, interventions, historical_monitoring, users.
