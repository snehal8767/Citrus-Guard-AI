"""AI image analysis route."""
import io
import os

from PIL import Image

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.ai.service import get_ai_service
from app.core.config import get_settings
from app.api.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/ai", tags=["ai"])

ALLOWED_TYPES = {"jpeg", "png", "webp", "bmp"}


@router.post("/analyze")
async def analyze_image(
    file: UploadFile,
    _: User = Depends(get_current_user),
):
    """Upload an image and run the real preprocessing + classifier pipeline."""
    settings = get_settings()

    # Read the full upload first (needed for both size check and validation).
    contents = await file.read()

    # Validate file type by decoding content (not just extension).
    try:
        with Image.open(io.BytesIO(contents)) as img:
            img.verify()
        with Image.open(io.BytesIO(contents)) as img:
            kind = (img.format or "").lower()
    except Exception:
        kind = "unknown"
    if kind not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image type '{kind}'. Allowed: {sorted(ALLOWED_TYPES)}",
        )
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max {settings.max_upload_mb} MB.",
        )

    # Save a copy to the uploads dir for traceability.
    os.makedirs(settings.upload_dir, exist_ok=True)
    safe_name = os.path.basename(file.filename or "upload.jpg")
    with open(os.path.join(settings.upload_dir, safe_name), "wb") as f:
        f.write(contents)

    service = get_ai_service()
    try:
        result = service.analyze_image(contents)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    result["filename"] = safe_name
    return result
