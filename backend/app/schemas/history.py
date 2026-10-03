"""History and metrics schemas."""
from datetime import datetime

from pydantic import BaseModel


class HistoryResponse(BaseModel):
    id: int
    orchard_id: int
    zone_id: int
    scan_id: int | None
    health_score: float
    risk_score: float
    affected_area: float
    recorded_at: datetime

    model_config = {"from_attributes": True}


class MetricsResponse(BaseModel):
    total_orchard_area: float
    monitored_area: float
    healthy_area: float
    at_risk_area: float
    critical_zones: int
    active_alerts: int
    latest_scan: datetime | None
    monitoring_coverage: float
    sensor_health: float
