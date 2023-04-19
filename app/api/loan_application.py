from fastapi import APIRouter, HTTPException
from app.models.loan_application import LoanApplication
from app.models.loan_application_update import LoanApplicationUpdate
from app.logging_config import configure_logging
from app.db.crud import LoanApplicationCRUD
from app.db.database import DatabaseConnection

logger = configure_logging(__name__)
router = APIRouter()

database_connection = DatabaseConnection()
crud = LoanApplicationCRUD(database_connection.SessionLocal())


class LoanApplicationAPI:
    def __init__(self):
        self.router = router

    @router.post("/loan_applications/")
    def create_loan_application(
            application: LoanApplication):
        try:
            logger.info("Creating loan application: %s", application)

            db_application = crud.create_loan_application(application)

            logger.info("Loan application created successfully")

            return db_application

        except Exception as e:
            logger.error("Error creating loan application: %s", e)
            raise HTTPException(
                status_code=500, detail="Error creating loan application")
        

    @router.get("/loan_applications/{application_id}/")
    def get_loan_application(application_id: int):
        try:
            logger.info("Getting loan application with ID: %s", application_id)

            db_application = crud.get_loan_application_by_id(
                application_id=application_id)

            if db_application is None:
                logger.warning(
                    "Loan application with ID %s not found", application_id)
                raise HTTPException(
                    status_code=404, detail="Application not found")

            logger.info("Loan application retrieved successfully")

            return db_application

        except HTTPException:
            raise  # re-raise HTTPException so FastAPI can handle it

        except Exception as e:
            logger.error("Error getting loan application: %s", e)
            raise HTTPException(
                status_code=500, detail="Error getting loan application")
        

    @router.put("/loan_applications/{application_id}/")
    def update_loan_application(
            application_id: int, application):
        try:
            logger.info("Updating loan application with ID: %s",
                        application_id)

            db_application = crud.update_loan_application(
                application_id, application)

            if db_application is None:
                logger.warning(
                    "Loan application with ID %s not found", application_id)
                raise HTTPException(
                    status_code=404, detail="Application not found")

            logger.info("Loan application updated successfully")

            return db_application

        except HTTPException:
            raise  # re-raise HTTPException so FastAPI can handle it

        except Exception as e:
            logger.error("Error updating loan application: %s", e)
            raise HTTPException(
                status_code=500, detail="Error updating loan application")
        

    @router.patch("/loan_applications/{application_id}/")
    def patch_loan_application(
        application_id: int, application: LoanApplicationUpdate
    ):
        try:
            logger.info("Patching loan application with ID: %s",
                        application_id)

            db_application = crud.patch_loan_application(
                application_id, application)

            if db_application is None:
                logger.warning(
                    "Loan application with ID %s not found", application_id)
                raise HTTPException(
                    status_code=404, detail="Application not found")

            logger.info("Loan application patched successfully")

            return db_application

        except HTTPException:
            raise  # re-raise HTTPException so FastAPI can handle it

        except Exception as e:
            logger.error("Error patching loan application: %s", e)
            raise HTTPException(
                status_code=500, detail="Error patching loan application")
        

    @router.delete("/loan_applications/{application_id}/")
    def delete_loan_application(application_id: int):
        try:
            logger.info("Deleting loan application with ID: %s",
                        application_id)

            success = crud.delete_loan_application(application_id)

            if not success:
                logger.warning(
                    "Loan application with ID %s not found", application_id)
                raise HTTPException(
                    status_code=404, detail="Application not found")

            logger.info("Loan application deleted successfully")

            return {"detail": "Application deleted"}

        except HTTPException:
            raise  # re-raise HTTPException so FastAPI can handle it

        except Exception as e:
            logger.error("Error deleting loan application: %s", e)
            raise HTTPException(
                status_code=500, detail="Error deleting loan application")
