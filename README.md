# HALO Backend

This is the backend service for the AI-powered recruitment and career intelligence platform.

# HALO Backend

FastAPI backend for HALO, an explainable career and recruitment intelligence platform.
The backend supports independent candidate workflows and company/HR workflows while
keeping resume evidence, candidate verification, and assessment evidence separate.

## Install dependencies

```bash
python -m venv .venv
. .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

## Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Health check

```bash
curl http://127.0.0.1:8000/health
```

## Swagger docs

Open http://127.0.0.1:8000/docs

## API reference

See [docs/API_INTEGRATION.md](docs/API_INTEGRATION.md) for the complete frontend integration
contract, authentication, ownership rules, request examples, lifecycle behavior, errors,
rate limiting, CORS, and intelligence endpoints.

The API is currently unversioned. Versioning was reviewed for Phase 19 and no `/api/v1`
prefix was added because existing clients use the current paths.

## Environment

Copy `.env.example` to `.env` and configure a non-default `JWT_SECRET_KEY` for production.
Set `ENVIRONMENT=production` in production. Configure explicit `CORS_ORIGINS`; do not use
wildcard origins with credentialed authentication. Optional GenAI configuration is server-side.

## Current API behavior

- Protected requests use `Authorization: Bearer <access_token>`.
- Roles are `COMPANY_ADMIN`, `HR`, and `CANDIDATE`.
- Unauthorized or cross-owner resources return `404` where ownership is hidden.
- Missing or invalid authentication returns `401`.
- Validation and lifecycle failures return `422`.
- Collections are currently bounded and do not use pagination.
- Rate-limited endpoints return `429` when configured limits are exceeded.
