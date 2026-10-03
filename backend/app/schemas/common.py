"""Shared Pydantic schemas."""
from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"
    demo_mode: bool
