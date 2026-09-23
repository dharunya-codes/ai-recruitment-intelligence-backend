from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").casefold()
SECRET_KEY = os.getenv("JWT_SECRET_KEY") or os.getenv("SECRET_KEY")
if not SECRET_KEY:
    if ENVIRONMENT == "production":
        raise RuntimeError("JWT_SECRET_KEY must be configured in production")
    SECRET_KEY = "dev-only-change-me"
if ENVIRONMENT == "production" and SECRET_KEY in {"change-me-in-production", "dev-only-change-me", "dev-secret-key"}:
    raise RuntimeError("A non-default JWT_SECRET_KEY must be configured in production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
if ALGORITHM != "HS256":
    raise RuntimeError("Only HS256 is supported by the configured JWT implementation")
if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
    raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str | int, role: str | None = None) -> str:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": str(subject), "exp": expire, "role": role}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    token_role = payload.get("role")
    if user_id is None or not isinstance(user_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id_value = int(user_id)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    user = db.query(User).filter(User.id == user_id_value).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if token_role != user.role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_candidate_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "CANDIDATE":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return current_user


def get_company_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in {"HR", "COMPANY_ADMIN"} or current_user.company_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company resource not found")
    return current_user
