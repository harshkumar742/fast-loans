from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud, database
from app.kafka.producer import produce_loan_application
from app.models.loan_application import LoanApplication
from app.models.loan_application_update import LoanApplicationUpdate

router = APIRouter()

# Dependency


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/loan_applications/")
async def create_loan_application(
    application: LoanApplication, db: Session = Depends(get_db)
):
    print(application)
    db_application = crud.create_loan_application(db, application)
    produce_loan_application(db_application)
    return db_application


@router.get("/loan_applications/{application_id}/")
def get_loan_application(application_id: int, db: Session = Depends(get_db)):
    db_application = crud.get_loan_application_by_id(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application


@router.put("/loan_applications/{application_id}/")
def update_loan_application(
    application_id: int, application, db: Session = Depends(get_db)
):
    db_application = crud.update_loan_application(db, application_id, application)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application


@router.patch("/loan_applications/{application_id}/")
def update_loan_application(
    application_id: int,
    application: LoanApplicationUpdate,
    db: Session = Depends(get_db),
):
    db_application = crud.get_loan_application_by_id(db, application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    update_data = application.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_application, key, value)

    db.commit()
    db.refresh(db_application)
    return db_application


@router.delete("/loan_applications/{application_id}/")
def delete_loan_application(application_id: int, db: Session = Depends(get_db)):
    success = crud.delete_loan_application(db, application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"detail": "Application deleted"}
