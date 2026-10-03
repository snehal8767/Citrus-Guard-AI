"""Alert routes: list, verify, reject, rescan."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import Alert, User
from app.schemas.alert import AlertResponse, VerificationResponse, VerifyRequest
from app.services import alert_service

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
def list_alerts(
    status: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Alert)
    if status:
        query = query.filter(Alert.status == status)
    return query.order_by(Alert.created_at.desc()).all()


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/{alert_id}/verify", response_model=AlertResponse)
def verify_alert(
    alert_id: int,
    payload: VerifyRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Human-in-the-loop: farmer verifies / rejects / requests rescan."""
    try:
        alert_service.record_verification(db, alert_id, payload.decision, payload.comment)
        db.commit()
        db.refresh(db.get(Alert, alert_id))
        return db.get(Alert, alert_id)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{alert_id}/reject", response_model=AlertResponse)
def reject_alert(
    alert_id: int,
    payload: VerifyRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        alert_service.record_verification(db, alert_id, "reject", payload.comment)
        db.commit()
        return db.get(Alert, alert_id)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{alert_id}/rescan", response_model=AlertResponse)
def rescan_alert(
    alert_id: int,
    payload: VerifyRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        alert_service.record_verification(db, alert_id, "rescan", payload.comment)
        db.commit()
        return db.get(Alert, alert_id)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
