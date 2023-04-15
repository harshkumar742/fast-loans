from fastapi import FastAPI
from app.db.models import LoanApplication
from app.db.database import engine, Base
from app.api import loan_application
from app.kafka.consumer import loan_application_consumer
import threading
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(loan_application.router, prefix="/api")


def run_consumer():
    loan_application_consumer()


if __name__ == "__main__":
    consumer_thread = threading.Thread(target=run_consumer, daemon=True)
    consumer_thread.start()

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
