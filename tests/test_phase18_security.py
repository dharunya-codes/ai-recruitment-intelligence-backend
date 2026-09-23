from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt

from app.database.database import SessionLocal
from app.main import app
from app.models.audit_event import AuditEvent
from app.models.report import Report
from app.services.rate_limit_service import rate_limiter
from app.utils.security import ALGORITHM, SECRET_KEY
from tests.test_assessment import _clear_phase10_data


client = TestClient(app)


def _clear() -> None:
    db = SessionLocal()
    try:
        db.query(AuditEvent).delete()
        db.query(Report).delete()
        db.commit()
    finally:
        db.close()
    _clear_phase10_data()
    rate_limiter.clear()


def _register_candidate(email: str) -> dict[str, str]:
    registered = client.post("/candidate/auth/register", json={"name": "Secure Candidate", "email": email, "password": "StrongPassword123"})
    assert registered.status_code == 200
    token = client.post("/candidate/auth/login", json={"email": email, "password": "StrongPassword123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_expired_invalid_signature_and_malformed_tokens_return_401() -> None:
    _clear()
    expired = jwt.encode({"sub": "1", "role": "CANDIDATE", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}, SECRET_KEY, algorithm=ALGORITHM)
    wrong_signature = jwt.encode({"sub": "1", "role": "CANDIDATE", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)}, "wrong-secret", algorithm=ALGORITHM)
    for token in (expired, wrong_signature, "not-a-jwt"):
        assert client.get("/candidate/resumes", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_security_headers_and_cors_are_restricted() -> None:
    _clear()
    response = client.get("/health")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    allowed = client.options("/health", headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"})
    blocked = client.options("/health", headers={"Origin": "https://untrusted.example", "Access-Control-Request-Method": "GET"})
    assert allowed.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert blocked.headers.get("access-control-allow-origin") is None


def test_rate_limiter_returns_429_when_configured_limit_is_exceeded(monkeypatch) -> None:
    _clear()
    monkeypatch.setenv("RATE_LIMIT_AUTH_PER_MINUTE", "1")
    first = client.post("/candidate/auth/login", json={"email": "missing@example.com", "password": "WrongPassword123"})
    second = client.post("/candidate/auth/login", json={"email": "missing@example.com", "password": "WrongPassword123"})
    assert first.status_code == 401
    assert second.status_code == 429
    monkeypatch.setenv("RATE_LIMIT_AUTH_PER_MINUTE", "120")
    rate_limiter.clear()


def test_career_question_enum_and_answer_limits_are_enforced() -> None:
    _clear()
    headers = _register_candidate("phase18-validation@example.com")
    invalid = client.post("/candidate/analysis/1/career-question", json={"question_type": "RUN_COMMAND"}, headers=headers)
    assert invalid.status_code == 422
    oversized = client.post("/candidate/analysis/1/career-question", json={"question_type": "X" * 81}, headers=headers)
    assert oversized.status_code == 422


def test_auth_audit_events_do_not_store_secrets() -> None:
    _clear()
    email = "phase18-audit@example.com"
    password = "StrongPassword123"
    registration = client.post("/candidate/auth/register", json={"name": "Audited", "email": email, "password": password})
    assert registration.status_code == 200
    client.post("/candidate/auth/login", json={"email": email, "password": password})
    client.post("/candidate/auth/login", json={"email": email, "password": "WrongPassword123"})
    db = SessionLocal()
    try:
        events = db.query(AuditEvent).all()
        event_types = {event.event_type for event in events}
        assert "REGISTRATION" in event_types
        assert "LOGIN_SUCCESS" in event_types
        assert "LOGIN_FAILURE" in event_types
        assert all(password not in str(event.__dict__) for event in events)
    finally:
        db.close()