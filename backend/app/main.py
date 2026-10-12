"""CitrusGuardAI FastAPI application entry point."""
import os
import subprocess
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    ai,
    alerts,
    auth,
    commands,
    history,
    interventions,
    metrics,
    orchards,
    reports,
    scans,
    sensors,
    zones,
)
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.schemas.common import HealthResponse

settings = get_settings()
setup_logging()

# The backend/ folder (contains alembic.ini and the app package).
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _bootstrap() -> None:
    """Prepare a fresh deployment at startup: migrate, seed, train the demo model.

    Makes the API self-sufficient on any host (Render, Railway, a fresh VM) —
    no manual shell steps needed. Each step is idempotent, so a normal restart
    is a fast no-op. Skipped entirely when AUTO_BOOTSTRAP=false (test suite).
    """
    if os.environ.get("AUTO_BOOTSTRAP", "true").strip().lower() in {
        "0",
        "false",
        "no",
        "off",
    }:
        print("[startup] auto-bootstrap disabled (AUTO_BOOTSTRAP=false)")
        return

    python = sys.executable

    try:
        print("[startup] Applying database migrations (alembic upgrade head)...")
        subprocess.run(
            [python, "-m", "alembic", "upgrade", "head"],
            cwd=BACKEND_ROOT,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"[startup] WARNING: migrations failed ({exc})")

    try:
        print("[startup] Seeding demo data (skips itself if not empty)...")
        subprocess.run(
            [python, "-m", "app.database.seed"],
            cwd=BACKEND_ROOT,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"[startup] WARNING: seed failed ({exc})")

    try:
        from app.ai.predictor import model_path

        if os.path.exists(model_path()):
            print("[startup] Demo model already present.")
        else:
            print("[startup] Training demo model...")
            subprocess.run(
                [python, "-m", "app.ai.train_demo_model"],
                cwd=BACKEND_ROOT,
                check=True,
            )
    except Exception as exc:  # model training must not block startup
        print(f"[startup] WARNING: demo model training failed ({exc})")

    print("[startup] Bootstrap complete.")


@asynccontextmanager
async def lifespan(_: FastAPI):
    _bootstrap()
    yield


app = FastAPI(
    title="CitrusGuardAI",
    description=(
        "AI-powered farm monitoring and automation for large orange orchards in Vidarbha, "
        "Maharashtra. Crop monitoring, pest/disease detection, orchard mapping, actionable alerts, "
        "precision intervention, farmer interface, and human-in-the-loop control."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health():
    return HealthResponse(status="ok", demo_mode=settings.demo_mode)


app.include_router(auth.router)
app.include_router(orchards.router)
app.include_router(zones.router)
app.include_router(scans.router)
app.include_router(ai.router)
app.include_router(sensors.router)
app.include_router(alerts.router)
app.include_router(interventions.router)
app.include_router(history.router)
app.include_router(metrics.router)
app.include_router(reports.router)
app.include_router(commands.router)


@app.get("/", tags=["health"])
def root():
    return {
        "name": "CitrusGuardAI",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
