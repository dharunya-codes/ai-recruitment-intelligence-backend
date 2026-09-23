from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
from ..models.common import BoundingBox, DeclarationStatus
from ..data.seed_data import SEED_BOUNDING_BOXES_0842

class BaseOCRService(ABC):
    """Abstract Base Class for OCR text and bounding box extraction."""

    @abstractmethod
    def extract_text_and_boxes(
        self, image_path_or_url: str
    ) -> Dict[str, Any]:
        """
        Extract raw text tokens and spatial bounding boxes from label image.
        Returns dictionary containing:
        - rawOcrTokensCount: int
        - boundingBoxes: List[BoundingBox]
        - processingTimeMs: int
        - confidenceScoreAvg: float
        """
        pass

class MockOCRService(BaseOCRService):
    """Realistic Mock OCR service producing calibrated coordinates & bounding boxes."""

    def extract_text_and_boxes(
        self, image_path_or_url: str
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        
        # In mock mode, return high quality recognized tokens & pre-calibrated boxes
        boxes: List[BoundingBox] = [
            BoundingBox(
                id=bb.id,
                x=bb.x,
                y=bb.y,
                width=bb.width,
                height=bb.height,
                label=bb.label,
                status=bb.status,
                confidence=bb.confidence,
            )
            for bb in SEED_BOUNDING_BOXES_0842
        ]
        
        elapsed_ms = int((time.perf_counter() - start) * 1000) + 380
        avg_confidence = round(
            sum(b.confidence for b in boxes) / len(boxes), 1
        ) if boxes else 96.0

        return {
            "rawOcrTokensCount": 124,
            "boundingBoxes": boxes,
            "processingTimeMs": elapsed_ms,
            "confidenceScoreAvg": avg_confidence,
        }

class PaddleOCRService(BaseOCRService):
    """Integration hook for PaddleOCR multilingual detection & recognition."""

    def __init__(self):
        # Placeholder for PaddleOCR instance:
        # from paddleocr import PaddleOCR
        # self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        self._initialized = False

    def extract_text_and_boxes(
        self, image_path_or_url: str
    ) -> Dict[str, Any]:
        # When active:
        # result = self.ocr.ocr(image_path_or_url, cls=True)
        # Convert bounding polygon -> normalized percentage BoundingBox
        return MockOCRService().extract_text_and_boxes(image_path_or_url)

class TesseractOCRService(BaseOCRService):
    """Integration hook for PyTesseract engine."""

    def __init__(self):
        self._initialized = False

    def extract_text_and_boxes(
        self, image_path_or_url: str
    ) -> Dict[str, Any]:
        # When active:
        # import pytesseract
        # data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        return MockOCRService().extract_text_and_boxes(image_path_or_url)

def get_ocr_service(engine: Optional[str] = None) -> BaseOCRService:
    if engine == "paddle_ocr":
        return PaddleOCRService()
    elif engine == "tesseract":
        return TesseractOCRService()
    return MockOCRService()
