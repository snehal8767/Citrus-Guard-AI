"""Intervention schemas."""
from datetime import datetime

from pydantic import BaseModel


class InterventionCreate(BaseModel):
    zone_id: int
    intervention_type: str
    target_area: float
    reason: str | None = None


class InterventionResponse(BaseModel):
    id: int
    zone_id: int
    intervention_type: str
    target_area: float
    status: str
    reason: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
