import pytest
from app.loan_approval import ApprovalCalculator
from app.db.models import LoanApplication

test_data = [
    {
        "credit_score": 750,
        "loan_amount": 50000,
        "loan_purpose": "business",
        "monthly_income": 8000,
        "monthly_debt": 2000,
        "employment_status": "employed",
        "risk_score": 20,
        "expected_approval": True,
    },
    {
        "credit_score": 800,
        "loan_amount": 500000,
        "loan_purpose": "other",
        "monthly_income": 80000,
        "monthly_debt": 12000,
        "employment_status": "unemployed",
        "risk_score": 60,
        "expected_approval": False,
    },
    {
        "credit_score": 600,
        "loan_amount": 50000,
        "loan_purpose": "debt_consolidation",
        "monthly_income": 8000,
        "monthly_debt": 2000,
        "employment_status": "employed",
        "risk_score": 60,
        "expected_approval": False,
    },
    {
        "credit_score": 700,
        "loan_amount": 150000,
        "loan_purpose": "debt_consolidation",
        "monthly_income": 0,
        "monthly_debt": 2000,
        "employment_status": "employed",
        "risk_score": 60,
        "expected_approval": False,
    },
]


@pytest.mark.parametrize("test_input", test_data)
def test_is_approved(test_input):
    application_data = LoanApplication(
        applicant_name="John Doe",
        credit_score=test_input["credit_score"],
        loan_amount=test_input["loan_amount"],
        loan_purpose=test_input["loan_purpose"],
        monthly_income=test_input["monthly_income"],
        monthly_debt=test_input["monthly_debt"],
        employment_status=test_input["employment_status"],
    )
    is_approved = ApprovalCalculator.is_approved(
        application_data, test_input["risk_score"]
    )
    assert is_approved == test_input["expected_approval"]
