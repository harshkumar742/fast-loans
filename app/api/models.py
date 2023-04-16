from typing import Optional
from pydantic import BaseModel, Field

class LoanApplication(BaseModel):
    id: Optional[int] = Field(None, ge=1)
    applicant_name: str = Field(..., min_length=1, max_length=255)
    credit_score: int = Field(..., ge=0, le=1000)
    loan_amount: float = Field(..., gt=0)
    loan_purpose: str = Field(..., min_length=1, max_length=255)
    monthly_income: float = Field(..., gt=0)
    monthly_debt: float = Field(..., ge=0)
    employment_status: str = Field(..., min_length=1, max_length=255)
    risk_score: Optional[int] = Field(None, ge=0, le=1000)
    is_approved: Optional[bool] = Field(None)
