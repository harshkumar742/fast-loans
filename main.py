import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.logging_config import configure_logging
from app.db.database import engine, Base
from app.api.loan_application import LoanApplicationAPI
from app.db.crud import LoanApplicationCRUD
from app.kafka.consumer import LoanApplicationConsumer
from app.db.database import DatabaseConnection
import threading
import uvicorn
import signal

# Create the database tables using SQLAlchemy
Base.metadata.create_all(bind=engine)

# Create a new FastAPI instance
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logger = configure_logging(__name__)

# Include the loan application API router
loan_api = LoanApplicationAPI()
app.include_router(loan_api.router, prefix="/api")

# Define a function to run the Kafka consumer in a separate thread
def run_consumer():
    logger.info("Starting Kafka consumer")
    consumer = LoanApplicationConsumer()
    try:
        consumer.consume_loan_application()
    except KeyboardInterrupt:
        logger.info("Kafka consumer interrupted. Shutting down gracefully...")
        consumer.stop()

# Check if the --consumer flag was passed in the command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--consumer", action="store_true", help="Run Kafka consumer only"
    )
    args = parser.parse_args()
    #args is args

    # If the --consumer flag was passed, run the Kafka consumer in two separate threads
    if args.consumer:
        for i in range(2):
            logger.info("Starting consumer thread %d", i)
            consumer_thread = threading.Thread(target=run_consumer)
            consumer_thread.start()
    # Otherwise, run the FastAPI application using Uvicorn
    else:
        logger.info("Starting FastAPI application")
        uvicorn.run(app)
