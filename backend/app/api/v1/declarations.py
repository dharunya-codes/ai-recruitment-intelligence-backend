from fastapi import APIRouter
from ...models.declaration import (
    ExtractDeclarationsRequest,
    ExtractDeclarationsResponse,
)
from ...services.ocr_service import get_ocr_service
from ...services.ai_model_service import get_ai_model_service

router = APIRouter(prefix="/declarations", tags=["Declarations"])

@router.post("/extract", response_model=ExtractDeclarationsResponse)
async def extract_declarations(request: ExtractDeclarationsRequest):
    """
    Dedicated OCR & AI Declaration Detection Pipeline:
    - Runs OCR token detection & spatial bounding box regression.
    - Classifies extracted text tokens into statutory declaration entities.
    """
    ocr_service = get_ocr_service(request.ocrEngine)
    ocr_result = ocr_service.extract_text_and_boxes(request.imageUrl)

    ai_service = get_ai_model_service()
    declarations = ai_service.extract_declarations(
        image_url=request.imageUrl,
        boxes=ocr_result["boundingBoxes"],
    )

    return ExtractDeclarationsResponse(
        fileId=request.fileId or "FILE-DEFAULT",
        rawOcrTokensCount=ocr_result["rawOcrTokensCount"],
        extractedDeclarations=declarations,
        boundingBoxes=ocr_result["boundingBoxes"],
        processingTimeMs=ocr_result["processingTimeMs"],
        confidenceScoreAvg=ocr_result["confidenceScoreAvg"],
    )
