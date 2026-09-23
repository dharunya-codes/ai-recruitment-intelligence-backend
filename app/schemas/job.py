from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    department: str | None = Field(default=None, max_length=150)
    location: str | None = Field(default=None, max_length=150)
    employment_type: str | None = Field(default=None, max_length=100)
    description: str = Field(..., min_length=1, max_length=100000)
    minimum_experience: str | None = None
    education: str | None = Field(default=None, max_length=255)
    certifications: str | None = None


class JobUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    department: str | None = Field(default=None, max_length=150)
    location: str | None = Field(default=None, max_length=150)
    employment_type: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=100000)
    minimum_experience: str | None = None
    education: str | None = Field(default=None, max_length=255)
    certifications: str | None = None


class JobResponse(BaseModel):
    id: int
    company_id: int
    title: str
    department: str | None
    location: str | None
    employment_type: str | None
    description: str | None
    minimum_experience: str | None
    education: str | None
    certifications: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)