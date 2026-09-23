import uvicorn
import os
import sys
from pathlib import Path

# Add backend directory to sys.path so app can be imported directly
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() in ("true", "1")

    print(f"============================================================")
    print(f"Starting LM-Inspect AI Backend Server...")
    print(f"URL: http://localhost:{port}")
    print(f"API Base: http://localhost:{port}/api/v1")
    print(f"Swagger Docs: http://localhost:{port}/docs")
    print(f"Redoc Docs: http://localhost:{port}/redoc")
    print(f"============================================================")

    uvicorn.run("app.main:app", host=host, port=port, reload=reload)
