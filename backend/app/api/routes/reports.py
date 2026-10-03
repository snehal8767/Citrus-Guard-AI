"""Report route: downloadable HTML report."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import User
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_class=HTMLResponse)
def download_report(
    orchard_id: int = 1,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        html = report_service.generate_html_report(db, orchard_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return HTMLResponse(content=html)
