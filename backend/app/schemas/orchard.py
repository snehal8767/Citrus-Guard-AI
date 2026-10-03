"""Orchard and zone schemas."""
from datetime import datetime

from pydantic import BaseModel, Field


class ZoneBase(BaseModel):
    zone_name: str
    area: float
    latitude: float
    longitude: float
    health_status: str = "Healthy"
    risk_score: float = Field(default=0.0, ge=0, le=100)


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    zone_name: str | None = None
    area: float | None = None
    health_status: str | None = None
    risk_score: float | None = Field(default=None, ge=0, le=100)


class ZoneResponse(ZoneBase):
    id: int
    orchard_id: int

    model_config = {"from_attributes": True}


class OrchardBase(BaseModel):
    name: str
    location: str | None = None
    area: float
    crop: str = "Orange (Nagpur Santra)"


class OrchardCreate(OrchardBase):
    pass


class OrchardUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    area: float | None = None
    crop: str | None = None


class OrchardResponse(OrchardBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class OrchardDetailResponse(OrchardResponse):
    zones: list[ZoneResponse] = []
