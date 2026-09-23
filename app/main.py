from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.auth import candidate_router as candidate_auth_router, router as auth_router
from app.api.assessment import router as assessment_router
from app.api.companies import router as companies_router
from app.api.jobs import router as jobs_router
from app.api.resumes import router as resumes_router
from app.api.reports import router as reports_router
from app.api.candidate import router as candidate_router
from app.api.intelligence import router as intelligence_router
from app.api.verification import router as verification_router
from app.database.init_db import init_db
from app.services.rate_limit_service import rate_limiter


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        init_db()
    except Exception as exc:  # pragma: no cover - DB may not be available yet
        print(f"Startup database init skipped: {exc}")
    yield


app = FastAPI(
    title="HALO Backend",
    version="0.1.0",
    description="AI-powered recruitment and career intelligence platform backend.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

configured_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
cors_origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_and_rate_limit(request: Request, call_next):
    path = request.url.path
    client_host = request.client.host if request.client else "unknown"
    bucket = None
    limit = 0
    if path in {"/auth/login", "/candidate/auth/login"}:
        bucket, limit = "auth", int(os.getenv("RATE_LIMIT_AUTH_PER_MINUTE", "120"))
    elif path in {"/auth/register", "/candidate/auth/register"}:
        bucket, limit = "registration", int(os.getenv("RATE_LIMIT_REGISTRATION_PER_MINUTE", "60"))
    elif path.endswith("/resumes") and request.method == "POST":
        bucket, limit = "upload", int(os.getenv("RATE_LIMIT_UPLOAD_PER_MINUTE", "60"))
    elif any(marker in path for marker in ("/generate", "/regenerate", "/career-question", "/multi-job")):
        bucket, limit = "expensive", int(os.getenv("RATE_LIMIT_EXPENSIVE_PER_MINUTE", "120"))
    if bucket and limit > 0 and not rate_limiter.allow(client_host, bucket, limit):
        response = JSONResponse(status_code=429, content={"detail": "Too many requests; please try again later"})
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

app.include_router(auth_router)
app.include_router(candidate_auth_router)
app.include_router(assessment_router)
app.include_router(companies_router)
app.include_router(jobs_router)
app.include_router(resumes_router)
app.include_router(reports_router)
app.include_router(candidate_router)
app.include_router(intelligence_router)
app.include_router(verification_router)

init_db()


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
