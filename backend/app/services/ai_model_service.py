from abc import ABC, abstractmethod
from typing import List, Optional
from copy import deepcopy

from ..models.declaration import DeclarationField
from ..models.common import BoundingBox
from ..data.seed_data import SEED_DECLARATIONS_0842

class BaseAIModelService(ABC):
    """Abstract Base Class for AI Declaration Extraction & Classification Models."""

    @abstractmethod
    def extract_declarations(
        self,
        image_url: str,
        boxes: List[BoundingBox],
        product_hints: Optional[dict] = None,
    ) -> List[DeclarationField]:
        """
        Takes image and spatial bounding boxes to infer statutory declaration entities.
        """
        pass

class MockAIModelService(BaseAIModelService):
    """Mock AI model producing standard detected declarations with confidence."""

    def extract_declarations(
        self,
        image_url: str,
        boxes: List[BoundingBox],
        product_hints: Optional[dict] = None,
    ) -> List[DeclarationField]:
        # Return deep copy of canonical declarations
        declarations = [deepcopy(d) for d in SEED_DECLARATIONS_0842]
        
        # If product hints are passed, adjust some field extracted values
        if product_hints:
            name = product_hints.get("productName")
            mfg = product_hints.get("manufacturer")
            if name:
                for d in declarations:
                    if d.key == "generic_name":
                        d.extractedValue = name
            if mfg:
                for d in declarations:
                    if d.key == "manufacturer_details":
                        d.extractedValue = mfg
                        
        return declarations

class LayoutLMDeclarationService(BaseAIModelService):
    """Integration hook for LayoutLMv3 or Document Question Answering transformers."""

    def __init__(self, model_checkpoint: Optional[str] = None):
        self.model_checkpoint = model_checkpoint or "microsoft/layoutlmv3-base"
        self._model = None

    def extract_declarations(
        self,
        image_url: str,
        boxes: List[BoundingBox],
        product_hints: Optional[dict] = None,
    ) -> List[DeclarationField]:
        # Ready for huggingface pipeline / transformers inference
        return MockAIModelService().extract_declarations(image_url, boxes, product_hints)

def get_ai_model_service() -> BaseAIModelService:
    return MockAIModelService()
