from pathlib import Path
from typing import List
import os

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME: str = "LM-Inspect AI - Legal Metrology Compliance Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Uploads directory
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads")))
    
    # Allowed CORS Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    # Host & Port
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Rule engine version
    RULES_ENGINE_VERSION: str = "LMPC-2011-RulesEngine-Rev2024.1"
    OCR_ENGINE_DEFAULT: str = "PaddleOCR High-Resolution Multilingual + LayoutLMv3"

settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
