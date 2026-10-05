"""Zone CRUD routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import OrchardZone, User
from app.schemas.orchard import ZoneCreate, ZoneResponse, ZoneUpdate
from app.schemas.recommendation import RecommendationResponse
from app.services import recommendation as recommendation_service

router = APIRouter(prefix="/zones", tags=["zones"])


@router.get("", response_model=list[ZoneResponse])
def list_zones(orchard_id: int | None = None, db: Session = Depends(get_db),
               _: User = Depends(get_current_user)):
    query = db.query(OrchardZone)
    if orchard_id is not None:
        query = query.filter(OrchardZone.orchard_id == orchard_id)
    return query.all()


@router.post("", response_model=ZoneResponse, status_code=status.HTTP_201_CREATED)
def create_zone(
    payload: ZoneCreate,
    orchard_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    zone = OrchardZone(orchard_id=orchard_id, **payload.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


@router.get("/{zone_id}/recommendation", response_model=RecommendationResponse)
def get_recommendation(
    zone_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Structured dosage-free action plan for a zone (condition, risk, area, steps)."""
    try:
        return recommendation_service.build_recommendation(db, zone_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{zone_id}", response_model=ZoneResponse)
def get_zone(zone_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    zone = db.get(OrchardZone, zone_id)
    if zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone


@router.put("/{zone_id}", response_model=ZoneResponse)
def update_zone(
    zone_id: int,
    payload: ZoneUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    zone = db.get(OrchardZone, zone_id)
    if zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(zone, key, value)
    db.commit()
    db.refresh(zone)
    return zone


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zone(zone_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    zone = db.get(OrchardZone, zone_id)
    if zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")
    db.delete(zone)
    db.commit()
