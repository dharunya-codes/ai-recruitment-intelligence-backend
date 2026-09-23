from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=200)
    role: str = Field(..., min_length=2, max_length=50)
    company_name: str | None = Field(default=None, min_length=2, max_length=150)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    company_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
