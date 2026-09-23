from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompanyResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)