# HALO Backend

This is the backend service for the AI-powered recruitment and career intelligence platform.

## Phase 1

This phase includes the FastAPI foundation, health endpoint, and Swagger UI setup.

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
