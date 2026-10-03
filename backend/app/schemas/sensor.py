"""Sensor schemas."""
from datetime import datetime

from pydantic import BaseModel


class SensorReadingResponse(BaseModel):
    id: int
    zone_id: int
    soil_moisture: float
    temperature: float
    humidity: float
    leaf_wetness: float
    irrigation_status: str
    timestamp: datetime

    model_config = {"from_attributes": True}


class SensorStatus(BaseModel):
    zone_id: int
    zone_name: str
    soil_moisture: float
    temperature: float
    humidity: float
    leaf_wetness: float
    irrigation_status: str
    status: str  # Normal | Warning | Critical
    last_updated: datetime
