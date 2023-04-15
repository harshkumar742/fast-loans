import pytest
from app.risk_assessment import RiskCalculator
from app.db.models import LoanApplication

test_data = [
    {
        "credit_score": 650,
        "loan_amount": 50000,
        "loan_purpose": "Home",
        "monthly_income": 8000,
        "monthly_debt": 2000,
        "employment_status": "Employed",
        "expected_risk_score": 30
    },
    {
        "credit_score": 450,
        "loan_amount": 70000,
        "loan_purpose": "Debt_consolidation",
        "monthly_income": 5000,
        "monthly_debt": 3500,
        "employment_status": "Unemployed",
        "expected_risk_score": 95
    }
]

@pytest.mark.parametrize("test_input", test_data)
def test_calculate_risk(test_input):
    application_data = LoanApplication(
        applicant_name="John Doe",
        credit_score=test_input["credit_score"],
        loan_amount=test_input["loan_amount"],
        loan_purpose=test_input["loan_purpose"],
        monthly_income=test_input["monthly_income"],
        monthly_debt=test_input["monthly_debt"],
        employment_status=test_input["employment_status"]
    )
    risk_score = RiskCalculator.calculate_risk(application_data)
    assert risk_score == test_input["expected_risk_score"]
