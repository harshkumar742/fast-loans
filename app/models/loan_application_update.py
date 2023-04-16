from typing import Optional
from pydantic import BaseModel


class LoanApplicationUpdate(BaseModel):
    applicant_name: Optional[str]
    credit_score: Optional[int]
    loan_amount: Optional[float]
    loan_purpose: Optional[str]
    monthly_income: Optional[float]
    monthly_debt: Optional[float]
    employment_status: Optional[str]
    risk_score: Optional[int]
    is_approved: Optional[bool]
