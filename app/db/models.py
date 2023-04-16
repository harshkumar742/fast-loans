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

    def dict(self):
        return {
            'id': self.id,
            'applicant_name': self.applicant_name,
            'credit_score': self.credit_score,
            'loan_amount': self.loan_amount,
            'loan_purpose': self.loan_purpose,
            'monthly_income': self.monthly_income,
            'monthly_debt': self.monthly_debt,
            'employment_status': self.employment_status,
            'risk_score': self.risk_score,
            'is_approved': self.is_approved,
        }
