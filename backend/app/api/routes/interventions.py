"""Intervention routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import Intervention, User
from app.schemas.intervention import InterventionCreate, InterventionResponse
from app.services import alert_service

router = APIRouter(prefix="/interventions", tags=["interventions"])


@router.get("", response_model=list[InterventionResponse])
def list_interventions(
    zone_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Intervention)
    if zone_id is not None:
        query = query.filter(Intervention.zone_id == zone_id)
    return query.order_by(Intervention.created_at.desc()).all()


@router.post("", response_model=InterventionResponse, status_code=status.HTTP_201_CREATED)
def create_intervention(
    payload: InterventionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Create a precision intervention. Requires a Verified alert (human-in-the-loop)."""
    try:
        intervention = alert_service.create_intervention(
            db,
            zone_id=payload.zone_id,
            intervention_type=payload.intervention_type,
            target_area=payload.target_area,
            reason=payload.reason,
        )
        db.commit()
        db.refresh(intervention)
        return intervention
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
