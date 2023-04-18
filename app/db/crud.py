from sqlalchemy.orm import Session
from . import models
from app.kafka.producer import KafkaProducer


class LoanApplicationCRUD:
    def __init__(self, db: Session):
        self.db = db
        self.kafka_producer = KafkaProducer()

    def create_loan_application(self, application):
        db_application = models.LoanApplication(**application.dict())

        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)

        # Call the produce_loan_application method
        self.kafka_producer.produce_loan_application(db_application)

        return db_application

    def get_loan_application_by_id(self, application_id: int):
        return (
            self.db.query(models.LoanApplication)
            .filter(models.LoanApplication.id == application_id)
            .first()
        )

    def update_loan_application(self, application_id: int, application):
        db_application = (
            self.db.query(models.LoanApplication)
            .filter(models.LoanApplication.id == application_id)
            .first()
        )

        if db_application is None:
            return None

        for key, value in application.dict().items():
            if value is not None:
                setattr(db_application, key, value)

        self.db.commit()

        return db_application

    def patch_loan_application(self, application_id: int, application):
        db_application = (
            self.db.query(models.LoanApplication)
            .filter(models.LoanApplication.id == application_id)
            .first()
        )
        if db_application is None:
            return None

        update_data = application.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_application, key, value)

        self.db.commit()
        self.db.refresh(db_application)

        return db_application

    def delete_loan_application(self, application_id: int):
        db_application = (
            self.db.query(models.LoanApplication)
            .filter(models.LoanApplication.id == application_id)
            .first()
        )

        if db_application is None:
            return False

        self.db.delete(db_application)
        self.db.commit()

        return True
