"""CitrusGuardAI FastAPI application entry point."""
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

app = FastAPI(
    title="CitrusGuardAI",
    description=(
        "AI-powered farm monitoring and automation for large orange orchards in Vidarbha, "
        "Maharashtra. Crop monitoring, pest/disease detection, orchard mapping, actionable alerts, "
        "precision intervention, farmer interface, and human-in-the-loop control."
    ),
    version="1.0.0",
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
