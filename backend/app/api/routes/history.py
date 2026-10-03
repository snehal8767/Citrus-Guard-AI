"""History routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import HistoricalMonitoring, User
from app.schemas.history import HistoryResponse

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[HistoryResponse])
def list_history(
    orchard_id: int | None = None,
    zone_id: int | None = None,
    limit: int = 200,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(HistoricalMonitoring)
    if orchard_id is not None:
        query = query.filter(HistoricalMonitoring.orchard_id == orchard_id)
    if zone_id is not None:
        query = query.filter(HistoricalMonitoring.zone_id == zone_id)
    return query.order_by(HistoricalMonitoring.recorded_at.desc()).limit(limit).all()
