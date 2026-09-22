from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="HALO Backend",
    version="0.1.0",
    description="AI-powered recruitment and career intelligence platform backend.",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "message": "HALO backend is running"}


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to HALO backend API"}


@app.exception_handler(404)
async def not_found_exception_handler(_, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Not found"},
    )
