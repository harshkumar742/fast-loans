from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.api import loan_application
from app.kafka.consumer import loan_application_consumer
import threading
import os

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
    consumer_thread = threading.Thread(target=run_consumer, daemon=True)
    consumer_thread.start()

    import uvicorn
    uvicorn.run(app)
