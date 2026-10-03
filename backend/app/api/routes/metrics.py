"""Metrics route."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import User
from app.schemas.history import MetricsResponse
from app.services import metrics_service

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=MetricsResponse)
def get_metrics(
    orchard_id: int = 1,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        return metrics_service.compute_metrics(db, orchard_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
