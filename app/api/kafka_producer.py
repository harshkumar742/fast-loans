from confluent_kafka import Producer
from app.db.models import LoanApplication
import json
import os


def produce_loan_application(application: LoanApplication):
    # Initialize Kafka producer
    conf = {'bootstrap.servers': os.getenv("KAFKA_BROKER_URL")}
    producer = Producer(conf)

    # Serialize the loan application as JSON
    application_json = json.dumps(application.dict())

    # Produce the message to the Kafka topic
    producer.produce(os.getenv("KAFKA_TOPIC"), key=str(
        application.id), value=application_json)
    producer.flush()
