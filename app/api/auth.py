from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.company import Company
from app.models.candidate import Candidate
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.schemas.candidate import CandidateProfileResponse, CandidateRegisterRequest
from app.services.audit_service import record_audit_event
from app.utils.security import create_access_token, get_candidate_user, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

candidate_router = APIRouter(prefix="/candidate/auth", tags=["Candidate Authentication"])


@candidate_router.post("/register", response_model=dict)
def register_candidate(payload: CandidateRegisterRequest, db: Session = Depends(get_db)) -> dict:
    if db.query(User).filter(User.email == str(payload.email)).first():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    user = User(name=payload.name, email=str(payload.email), password_hash=hash_password(payload.password), role="CANDIDATE")
    db.add(user)
    db.flush()
    candidate = Candidate(user_id=user.id, name=payload.name, email=str(payload.email))
    db.add(candidate)
    db.commit()
    db.refresh(user)
    record_audit_event(db, "REGISTRATION", user_id=user.id, role=user.role, success=True)
    return {"message": "Candidate registration successful", "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role, "company_id": None}}


@candidate_router.post("/login", response_model=TokenResponse)
def login_candidate(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.email == str(payload.email), User.role == "CANDIDATE").first()
    if not user or not verify_password(payload.password, user.password_hash):
        record_audit_event(db, "LOGIN_FAILURE", success=False)
        raise HTTPException(status_code=401, detail="Invalid candidate email or password", headers={"WWW-Authenticate": "Bearer"})
    record_audit_event(db, "LOGIN_SUCCESS", user_id=user.id, role=user.role, success=True)
    return TokenResponse(access_token=create_access_token(subject=user.id, role=user.role))


@candidate_router.get("/me", response_model=CandidateProfileResponse)
def candidate_profile(current_user: User = Depends(get_candidate_user)) -> CandidateProfileResponse:
    return CandidateProfileResponse(id=current_user.id, name=current_user.name, email=current_user.email, role=current_user.role, created_at=current_user.created_at)


@router.post("/register", response_model=dict)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)) -> dict:
    if payload.role not in {"HR", "COMPANY_ADMIN"} or not payload.company_name:
        raise HTTPException(status_code=422, detail="Company registration requires role HR or COMPANY_ADMIN and company_name")
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    company = None
    if payload.company_name:
        company = Company(name=payload.company_name, email=payload.email)
        db.add(company)
        db.commit()
        db.refresh(company)

    user = User(
        company_id=company.id,
        name=payload.name,
        email=str(payload.email),
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "company_id": user.company_id,
        },
    }


@router.post("/login", response_model=TokenResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.email == str(payload.email)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        record_audit_event(db, "LOGIN_FAILURE", success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    record_audit_event(db, "LOGIN_SUCCESS", user_id=user.id, role=user.role, success=True)
    token = create_access_token(subject=user.id, role=user.role)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
        company_id=current_user.company_id,
    )
