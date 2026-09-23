from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class JDUploadRequest(BaseModel):
    description: str = Field(..., min_length=10, max_length=100000)


class JobRequirementResponse(BaseModel):
    id: int
    job_id: int
    requirement: str
    category: str
    importance: str | None

    model_config = ConfigDict(from_attributes=True)


class JobRequirementsResponse(BaseModel):
    job_id: int
    requirements: list[JobRequirementResponse]