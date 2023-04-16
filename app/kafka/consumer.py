from confluent_kafka import Consumer, KafkaError
from app.risk_assessment import RiskCalculator
from app.loan_approval import ApprovalCalculator
from app.db.models import LoanApplication
from app.db import crud, database
import os
import json


def loan_application_consumer():
    conf = {
        'bootstrap.servers': os.getenv("KAFKA_BROKER_URL"),
        'security.protocol': os.getenv('KAFKA_SEC_PROTOCOL'),
        'sasl.mechanisms': os.getenv('KAFKA_SASL_MECH'),
        'sasl.username': os.getenv('KAFKA_USERNAME'),
        'sasl.password': os.getenv('KAFKA_PASSWORD'),
        'group.id': 'loan_approval_group'
    }
    consumer = Consumer(conf)
    consumer.subscribe([os.getenv("KAFKA_TOPIC")])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        if msg.error():
            print(f"Error: {msg.error()}")
        else:
            application_data = json.loads(msg.value())
            application = LoanApplication(**application_data)

            risk_score = RiskCalculator.calculate_risk(application)
            is_approved = ApprovalCalculator.is_approved(
                application, risk_score)

            application.risk_score = risk_score
            application.is_approved = is_approved

            with database.SessionLocal() as db:
                crud.update_loan_application(db, application.id, application)
