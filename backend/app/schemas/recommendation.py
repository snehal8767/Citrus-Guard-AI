"""Recommendation schemas."""
from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    zone_id: int
    zone_name: str
    health_status: str
    risk_score: float
    area: float
    condition: str
    severity: str
    risk: float
    affected_area: float
    alert_id: int | None
    alert_status: str | None
    verified_alert: bool
    steps: list[str]
    safety_note: str
