from fastapi.testclient import TestClient
from main import app
from app.db.models import LoanApplication

client = TestClient(app)

application_data = LoanApplication(
    applicant_name="John Doe",
    credit_score=750,
    loan_amount=50000,
    loan_purpose="business",
    monthly_income=8000,
    monthly_debt=2000,
    employment_status="employed",
)


def test_create_loan_application():
    response = client.post("api/loan_applications/", json=application_data.dict())
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["applicant_name"] == "John Doe"


def test_get_loan_application():
    response_post = client.post("api/loan_applications/", json=application_data.dict())
    application_id = response_post.json()["id"]

    response_get = client.get(f"api/loan_applications/{application_id}/")
    assert response_get.status_code == 200
    assert response_get.json()["applicant_name"] == "John Doe"


def test_update_loan_application():
    response_post = client.post("api/loan_applications/", json=application_data.dict())
    application_id = response_post.json()["id"]

    updated_data = {"applicant_name": "Jane Doe"}
    response_put = client.patch(
        f"api/loan_applications/{application_id}/", json=updated_data
    )
    assert response_put.status_code == 200
    assert response_put.json()["applicant_name"] == "Jane Doe"


def test_delete_loan_application():
    response_post = client.post("api/loan_applications/", json=application_data.dict())
    application_id = response_post.json()["id"]

    response_delete = client.delete(f"api/loan_applications/{application_id}/")
    assert response_delete.status_code == 200
    assert response_delete.json()["detail"] == "Application deleted"
