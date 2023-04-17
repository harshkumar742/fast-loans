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
    # Create a loan application with valid data
    response = client.post("api/loan_applications/", json=application_data.dict())
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["applicant_name"] == "John Doe"


def test_get_loan_application():
    # Retrieve a loan application with a valid ID
    response_post = client.post("api/loan_applications/", json=application_data.dict())
    application_id = response_post.json()["id"]

    response_get = client.get(f"api/loan_applications/{application_id}/")
    assert response_get.status_code == 200
    assert response_get.json()["applicant_name"] == "John Doe"


def test_update_loan_application():
    # Update a loan application with valid data
    response_post = client.post("api/loan_applications/", json=application_data.dict())
    application_id = response_post.json()["id"]

    updated_data = {"applicant_name": "Jane Doe"}
    response_put = client.patch(
        f"api/loan_applications/{application_id}/", json=updated_data
    )
    assert response_put.status_code == 200
    assert response_put.json()["applicant_name"] == "Jane Doe"


def test_patch_loan_application():
    # Patch a loan application with valid data
    response = client.post("/api/loan_applications/", json=application_data.dict())
    assert response.status_code == 200
    loan_application_id = response.json()["id"]

    updated_data = {"applicant_name": "Jane Doe"}
    response = client.patch(
        f"/api/loan_applications/{loan_application_id}/", json=updated_data
    )
    assert response.status_code == 200

    response = client.get(f"/api/loan_applications/{loan_application_id}/")
    assert response.status_code == 200
    assert response.json()["applicant_name"] == "Jane Doe"


def test_delete_loan_application():
    # Delete a loan application with a valid ID
    response_post = client.post("api/loan_applications/", json=application_data.dict())
    application_id = response_post.json()["id"]

    response_delete = client.delete(f"api/loan_applications/{application_id}/")
    assert response_delete.status_code == 200
    assert response_delete.json()["detail"] == "Application deleted"


def test_create_loan_application_error():
    # Try to create a loan application with invalid data
    invalid_data = application_data.dict()
    invalid_data["credit_score"] = -1
    response = client.post("/api/loan_applications/", json=invalid_data)
    assert response.status_code == 422


def test_get_loan_application_error():
    # Try to retrieve a loan application with an invalid ID
    invalid_id = 999999
    response = client.get(f"/api/loan_applications/{invalid_id}/")
    assert response.status_code == 404


def test_update_loan_application_error():
    # Try to update a loan application with invalid data
    response_post = client.post("/api/loan_applications/", json=application_data.dict())
    application_id = response_post.json()["id"]
    invalid_data = {"credit_score": -1}
    response_put = client.put(
        f"/api/loan_applications/{application_id}/", json=invalid_data
    )
    assert response_put.status_code == 422


def test_patch_loan_application_error():
    # Try to patch a loan application with an invalid ID
    invalid_id = 999999
    updated_data = {"applicant_name": "Jane Doe"}
    response = client.patch(f"/api/loan_applications/{invalid_id}/", json=updated_data)
    assert response.status_code == 404

    # Try to patch a loan application with invalid data
    response_post = client.post("/api/loan_applications/", json=application_data.dict())
    application_id = response_post.json()["id"]
    invalid_data = {"credit_score": "w"}
    response_patch = client.patch(
        f"/api/loan_applications/{application_id}/", json=invalid_data
    )
    assert response_patch.status_code == 422


def test_delete_loan_application_error():
    # Try to delete a loan application with an invalid ID
    invalid_id = 999999
    response_delete = client.delete(f"/api/loan_applications/{invalid_id}/")
    assert response_delete.status_code == 404
