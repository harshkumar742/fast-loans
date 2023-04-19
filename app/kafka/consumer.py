from confluent_kafka import Consumer, KafkaError
from app.risk_assessment import RiskCalculator
from app.loan_approval import ApprovalCalculator
from app.db.models import LoanApplication
from app.db import database
import os
import json
from app.logging_config import configure_logging
from app.db.crud import LoanApplicationCRUD

logger = configure_logging(__name__)


class LoanApplicationConsumer:
    def __init__(self):
        conf = {
            "bootstrap.servers": os.getenv("KAFKA_BROKER_URL"),
            "security.protocol": os.getenv("KAFKA_SEC_PROTOCOL"),
            "sasl.mechanisms": os.getenv("KAFKA_SASL_MECH"),
            "sasl.username": os.getenv("KAFKA_USERNAME"),
            "sasl.password": os.getenv("KAFKA_PASSWORD"),
            "group.id": "loan_approval_group",
        }

        self.consumer = Consumer(conf)
        self.consumer.subscribe([os.getenv("KAFKA_TOPIC")])
        self.is_running = True

    def consume_loan_application(self):
        with database.SessionLocal() as db:
            crud_instance = LoanApplicationCRUD(db)

        while True:
            try:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    logger.error(f"Error: {msg.error()}")
                else:
                    application_data = json.loads(msg.value())
                    application = LoanApplication(**application_data)

                    risk_score = RiskCalculator.calculate_risk(application)
                    is_approved = ApprovalCalculator.is_approved(
                        application, risk_score)

                    application.risk_score = risk_score
                    application.is_approved = is_approved

                    crud_instance.update_loan_application(
                        application.id, application)

                    logger.info(
                        f"Loan application with ID {application.id} processed successfully"
                    )

            except Exception as e:
                logger.error(f"Error consuming loan application: {str(e)}")
                continue


    def stop(self):
        logger.info("Stopping Kafka consumer")

        self.is_running = False
        self.consumer.close()
