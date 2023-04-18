from confluent_kafka import Producer
from app.db.models import LoanApplication
import json
import os
from app.logging_config import configure_logging

logger = configure_logging(__name__)


class KafkaProducer:
    def __init__(self):
        # Initialize Kafka producer
        self.conf = {
            "bootstrap.servers": os.getenv("KAFKA_BROKER_URL"),
            "security.protocol": os.getenv("KAFKA_SEC_PROTOCOL"),
            "sasl.mechanisms": os.getenv("KAFKA_SASL_MECH"),
            "sasl.username": os.getenv("KAFKA_USERNAME"),
            "sasl.password": os.getenv("KAFKA_PASSWORD"),
        }
        self.producer = Producer(self.conf)

    def produce_loan_application(self, application: LoanApplication):
        try:
            # Serialize the loan application as JSON
            application_dict = {
                column.name: getattr(application, column.name)
                for column in application.__table__.columns
            }
            application_json = json.dumps(application_dict)

            # Produce the message to the Kafka topic
            self.producer.produce(
                os.getenv("KAFKA_TOPIC"), key=str(application.id), value=application_json
            )
            self.producer.flush()

            logger.info(
                f"Produced loan application with ID {application.id} to Kafka topic"
            )

        except Exception as e:
            logger.error(
                f"Error producing loan application with ID {application.id} to Kafka topic: {e}"
            )
