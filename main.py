import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.logging_config import configure_logging
from app.db.database import engine, Base
from app.api import loan_application
from app.kafka.consumer import loan_application_consumer
import threading
import uvicorn

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
app.include_router(loan_application.router, prefix="/api")


# Define a function to run the Kafka consumer in a separate thread
def run_consumer():
    logger.info("Starting Kafka consumer")
    loan_application_consumer()


# Check if the --consumer flag was passed in the command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--consumer", action="store_true", help="Run Kafka consumer only"
    )
    args = parser.parse_args()

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
