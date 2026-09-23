from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    file_name: str
    candidate_name: str
    candidate_email: str
    candidate_phone: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeTextResponse(BaseModel):
    resume_id: int
    extracted_text: str