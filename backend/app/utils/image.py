import base64
from fastapi import UploadFile, HTTPException
from ..config import settings

def validate_image(file: UploadFile):
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported image type: {file.content_type}. Allowed: {settings.ALLOWED_MIME_TYPES}"
        )

async def encode_image(file: UploadFile) -> str:
    """Read image and return base64 string without data prefix."""
    content = await file.read()
    
    # Simple size check
    if len(content) > settings.MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"Image size exceeds {settings.MAX_IMAGE_SIZE_MB}MB limit."
        )
        
    return base64.b64encode(content).decode("utf-8")
