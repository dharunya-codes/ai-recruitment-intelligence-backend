from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resume_id: int
    report_type: str
    generation_status: str
    report_data: dict[str, Any]
    created_at: datetime


class ReportsResponse(BaseModel):
    resume_id: int
    reports: dict[str, ReportResponse]