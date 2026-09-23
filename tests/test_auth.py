from fastapi.testclient import TestClient

from app.main import app
from app.database.database import SessionLocal
from app.models.company import Company
from app.models.user import User

client = TestClient(app)


def _clear_users_and_companies() -> None:
    db = SessionLocal()
    try:
        db.query(User).delete()
        db.query(Company).delete()
        db.commit()
    finally:
        db.close()


def test_register_success() -> None:
    _clear_users_and_companies()
    payload = {
        "name": "Yuthika",
        "email": "yuthika@example.com",
        "password": "StrongPassword123",
        "role": "COMPANY_ADMIN",
        "company_name": "Example Company",
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Registration successful"
    assert body["user"]["email"] == "yuthika@example.com"
    assert body["user"]["role"] == "COMPANY_ADMIN"
    assert "password" not in body["user"]
    assert "password_hash" not in body["user"]


def test_duplicate_email_rejected() -> None:
    _clear_users_and_companies()
    payload = {
        "name": "Yuthika",
        "email": "duplicate@example.com",
        "password": "StrongPassword123",
        "role": "COMPANY_ADMIN",
        "company_name": "Example Company",
    }

    first = client.post("/auth/register", json=payload)
    assert first.status_code == 200

    second = client.post("/auth/register", json=payload)
    assert second.status_code == 400
    assert "already exists" in second.json()["detail"].lower()


def test_password_is_hashed_and_not_plaintext() -> None:
    _clear_users_and_companies()
    payload = {
        "name": "Test HR",
        "email": "hashcheck@example.com",
        "password": "TestPassword123",
        "role": "HR",
        "company_name": "HALO Demo Company",
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "hashcheck@example.com").first()
        assert user is not None
        assert user.password_hash != "TestPassword123"
        assert user.password_hash.startswith("$2")
    finally:
        db.close()


def test_login_success_and_token() -> None:
    _clear_users_and_companies()
    client.post(
        "/auth/register",
        json={
            "name": "Test HR",
            "email": "login@example.com",
            "password": "TestPassword123",
            "role": "HR",
            "company_name": "HALO Demo Company",
        },
    )

    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "TestPassword123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_fails_with_invalid_password() -> None:
    _clear_users_and_companies()
    client.post(
        "/auth/register",
        json={
            "name": "Test HR",
            "email": "badlogin@example.com",
            "password": "CorrectPassword123",
            "role": "HR",
            "company_name": "HALO Demo Company",
        },
    )

    response = client.post(
        "/auth/login",
        json={"email": "badlogin@example.com", "password": "WrongPassword123"},
    )
    assert response.status_code == 401


def test_auth_me_requires_valid_token() -> None:
    _clear_users_and_companies()
    token_response = client.post(
        "/auth/register",
        json={
            "name": "Test HR",
            "email": "me@example.com",
            "password": "TestPassword123",
            "role": "HR",
            "company_name": "HALO Demo Company",
        },
    )
    assert token_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={"email": "me@example.com", "password": "TestPassword123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    authed = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert authed.status_code == 200
    assert authed.json()["email"] == "me@example.com"
    assert "password_hash" not in authed.json()

    missing = client.get("/auth/me")
    assert missing.status_code == 401

    invalid = client.get("/auth/me", headers={"Authorization": "Bearer invalid-token"})
    assert invalid.status_code == 401
