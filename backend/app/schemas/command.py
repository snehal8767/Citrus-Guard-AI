"""Command console schemas."""
from pydantic import BaseModel


class CommandRequest(BaseModel):
    command: str


class CommandResponse(BaseModel):
    intent: str
    message: str
    data: dict | list | None = None
