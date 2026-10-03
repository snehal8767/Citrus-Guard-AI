"""Scan and detection schemas."""
from datetime import datetime

from pydantic import BaseModel, Field


class ScanCreate(BaseModel):
    orchard_id: int
    scan_type: str = "drone_simulation"


class AIDetectionResponse(BaseModel):
    id: int
    scan_id: int
    zone_id: int
    condition: str
    confidence: float
    severity: str
    explanation: str | None
    timestamp: datetime

    model_config = {"from_attributes": True}


class ScanResponse(BaseModel):
    id: int
    orchard_id: int
    scan_type: str
    timestamp: datetime
    coverage: float
    status: str
    detections: list[AIDetectionResponse] = []

    model_config = {"from_attributes": True}
