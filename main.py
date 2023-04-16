import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.db.database import engine, Base
from app.api import loan_application
from app.kafka.consumer import loan_application_consumer
import threading

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(loan_application.router, prefix="/api")


def run_consumer():
    loan_application_consumer()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--consumer', action='store_true', help='Run Kafka consumer only')
    args = parser.parse_args()

    if args.consumer:
        for i in range(2):
            print("Consumer started: ", i)
            consumer_thread = threading.Thread(target=run_consumer, daemon=True)
            consumer_thread.start()
    else:
        uvicorn.run(app)
