"""Orchard CRUD routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import Orchard, User
from app.schemas.orchard import OrchardCreate, OrchardDetailResponse, OrchardResponse, OrchardUpdate

router = APIRouter(prefix="/orchards", tags=["orchards"])


@router.get("", response_model=list[OrchardResponse])
def list_orchards(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Orchard).all()


@router.post("", response_model=OrchardResponse, status_code=status.HTTP_201_CREATED)
def create_orchard(
    payload: OrchardCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    orchard = Orchard(**payload.model_dump())
    db.add(orchard)
    db.commit()
    db.refresh(orchard)
    return orchard


@router.get("/{orchard_id}", response_model=OrchardDetailResponse)
def get_orchard(
    orchard_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    orchard = db.get(Orchard, orchard_id)
    if orchard is None:
        raise HTTPException(status_code=404, detail="Orchard not found")
    return orchard


@router.put("/{orchard_id}", response_model=OrchardResponse)
def update_orchard(
    orchard_id: int,
    payload: OrchardUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    orchard = db.get(Orchard, orchard_id)
    if orchard is None:
        raise HTTPException(status_code=404, detail="Orchard not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(orchard, key, value)
    db.commit()
    db.refresh(orchard)
    return orchard


@router.delete("/{orchard_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_orchard(
    orchard_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    orchard = db.get(Orchard, orchard_id)
    if orchard is None:
        raise HTTPException(status_code=404, detail="Orchard not found")
    db.delete(orchard)
    db.commit()
