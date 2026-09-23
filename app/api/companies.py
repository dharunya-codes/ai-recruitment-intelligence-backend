from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyResponse
from app.utils.security import get_company_user

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/me", response_model=CompanyResponse)
def get_my_company(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> Company:
    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    return company