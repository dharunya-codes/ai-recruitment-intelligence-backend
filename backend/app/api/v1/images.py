import os
import uuid
from typing import Optional
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image

from ...config import settings
from ...models.report import UploadImageResponse

router = APIRouter(prefix="/images", tags=["Images"])

@router.post("/upload", response_model=UploadImageResponse)
async def upload_product_image(
    image: UploadFile = File(...),
    scanType: Optional[str] = Form(None),
):
    """
    Ingest packaging image for Computer Vision / OCR analysis.
    Saves image to uploads directory and returns file metadata.
    """
    file_ext = Path(image.filename or "image.jpg").suffix.lower()
    if not file_ext:
        file_ext = ".jpg"
        
    unique_id = f"FILE-{int(uuid.uuid4().time_low)}"
    saved_filename = f"{unique_id}{file_ext}"
    destination = settings.UPLOAD_DIR / saved_filename

    try:
        contents = await image.read()
        with open(destination, "wb") as f:
            f.write(contents)
            
        # Inspect resolution using Pillow
        width, height, dpi = 2400, 3000, 300
        try:
            with Image.open(destination) as img:
                width, height = img.size
                dpi_info = img.info.get("dpi")
                if dpi_info and isinstance(dpi_info, tuple):
                    dpi = int(dpi_info[0])
        except Exception:
            pass

        # Construct accessible static URL
        image_url = f"/uploads/{saved_filename}"

        return UploadImageResponse(
            fileId=unique_id,
            imageUrl=image_url,
            filename=image.filename or saved_filename,
            format=image.content_type or "image/jpeg",
            resolution={"width": width, "height": height, "dpi": dpi},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
