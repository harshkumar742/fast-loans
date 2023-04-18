from sqlalchemy.orm import Session
from . import models


def create_loan_application(db: Session, application):
    db_application = models.LoanApplication(**application.dict())

    db.add(db_application)
    db.commit()

    db.refresh(db_application)

    return db_application


def get_loan_application_by_id(db: Session, application_id: int):
    return (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.id == application_id)
        .first()
    )


def update_loan_application(db: Session, application_id: int, application):
    db_application = (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.id == application_id)
        .first()
    )

    if db_application is None:
        return None

    for key, value in application.dict().items():
        if value is not None:
            setattr(db_application, key, value)

    db.commit()

    return db_application


def patch_loan_application(db: Session, application_id: int, application):
    db_application = (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.id == application_id)
        .first()
    )

    if db_application is None:
        return None

    update_data = application.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_application, key, value)

    db.commit()
    db.refresh(db_application)

    return db_application


def delete_loan_application(db: Session, application_id: int):
    db_application = (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.id == application_id)
        .first()
    )

    if db_application is None:
        return False

    db.delete(db_application)
    db.commit()

    return True
