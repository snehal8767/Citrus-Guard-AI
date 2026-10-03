"""Alert and verification schemas."""
from datetime import datetime

from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: int
    zone_id: int
    alert_type: str
    severity: str
    risk_score: float
    message: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class VerifyRequest(BaseModel):
    decision: str  # verify | reject | rescan
    comment: str | None = None


class VerificationResponse(BaseModel):
    id: int
    alert_id: int
    decision: str
    comment: str | None
    timestamp: datetime

    model_config = {"from_attributes": True}
