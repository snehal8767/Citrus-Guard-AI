"""Image analysis schemas."""
from datetime import datetime

from pydantic import BaseModel


class ImageAnalysisResponse(BaseModel):
    id: int
    filename: str
    condition: str
    confidence: float
    severity: str
    explanation: str | None
    next_step: str | None
    model_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
