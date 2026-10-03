"""Scan routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import Scan, User
from app.schemas.scan import ScanCreate, ScanResponse
from app.services import scan_service

router = APIRouter(prefix="/scans", tags=["scans"])


@router.get("", response_model=list[ScanResponse])
def list_scans(orchard_id: int | None = None, db: Session = Depends(get_db),
               _: User = Depends(get_current_user)):
    query = db.query(Scan)
    if orchard_id is not None:
        query = query.filter(Scan.orchard_id == orchard_id)
    return query.order_by(Scan.timestamp.desc()).all()


@router.post("", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
def create_scan(
    payload: ScanCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        scan = scan_service.run_scan(db, payload.orchard_id, payload.scan_type)
        db.commit()
        db.refresh(scan)
        return scan
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{scan_id}", response_model=ScanResponse)
def get_scan(scan_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    scan = db.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan
