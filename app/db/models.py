from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.database import Base

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    applicant_name = Column(String(255))
    credit_score = Column(Integer)
    loan_amount = Column(Float)
    loan_purpose = Column(String(255))
    monthly_income = Column(Float)
    monthly_debt = Column(Float)
    employment_status = Column(String(255))
    risk_score = Column(Integer)
    is_approved = Column(Boolean)
