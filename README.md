
# Fast Loans

A simplified, scalable loan approval system that can evaluate loan applications, calculate the risk of lending, and approve or reject applications based on predefined criteria.

## Frontend

A basic frontend for the Fast Loans project is available at the following URL:

[https://main.d221526vcnzerk.amplifyapp.com/](https://main.d221526vcnzerk.amplifyapp.com/)

Visit the link to interact with the loan application system through a web interface.

## Table of Contents
- [High Level System Design](#high-level-system-design)
- [Requirements](#requirements)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Logging](#logging)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database Model](#database-model)
- [Contribution](#contribution)
- [License](#license)
- [Deployment](#deployment)
  - [Heroku](#heroku)
  - [AWS](#aws)
- [Support](#support)
- [Acknowledgements](#acknowledgements)
- [Authors](#authors)

## High Level System Design
![Architecture Diagram]()
### Components
1. **Load Balancer**: Distributes incoming traffic among multiple instances of the Uvicorn server.
2. **API Layer**: FastAPI with multiple instances of the Uvicorn server, each having multiple workers, is used to create RESTful API endpoints to handle CRUD operations (Create, Read, Update, Delete) for loan applications.
3. **Cache Layer**: Redis can be used as a caching layer to store frequently accessed data, reducing the load on the PostgreSQL database. Not Implemented.
4. **Message Queue**: Kafka is used for processing loan applications asynchronously. Loan applications are sent to the Kafka producer, which will be consumed by multiple Kafka consumers for scaling.
5. **Database Layer**: PostgreSQL with replication is used as the RDS database to store loan applications and their associated data.
6. **Risk Assessment Module**: Calculates the risk score for each loan application.
7. **Loan Approval Module**: Evaluates the risk score and approves or rejects loan applications based on predefined criteria.

### Rough Capacity Estimation for "Fast Loans" Application

To perform a rough capacity estimation for "Fast Loans" application with 1 million users and 1 application per user per day, we'll make a few assumptions and estimations on the expected usage and requirements. These numbers are rough estimates and can be adjusted based on our specific use case.

**Assumptions**:

- Number of daily active users (DAU): 1,000,000
- Number of loan applications per user per day: 1
- Average size of a loan application record: 1 KB (considering all fields and metadata)
- Read/Write ratio: 80% read and 20% write

**Calculations**:

- Loan applications per day: 1,000,000 users * 1 application/user = 1,000,000 loan applications
- Storage requirement per day: 1,000,000 loan applications * 1 KB/application = 1,000,000 KB = 1,000 MB = 1 GB
- Storage requirement for 30 days: 1 GB/day * 30 days = 30 GB

**Traffic Estimation**:

- Total requests per day: 1,000,000 loan applications * (80% read + 20% write) = 2,000,000 requests
- Requests per second (peak): (2,000,000 requests/day) / (24 hours * 3600 seconds) * 2 (assuming a 2x peak factor) ≈ 46 requests/sec

**Bandwidth Estimation**:

- Data in per second (peak): 46 requests/sec * 1 KB (write) * 20% = 9.2 KB/sec
- Data out per second (peak): 46 requests/sec * 1 KB (read) * 80% = 36.8 KB/sec

With these rough capacity estimations, we can plan your infrastructure, scaling, and caching strategies accordingly. These numbers are based on assumptions and should be adjusted and monitored as needed based on real-world usage patterns.

### Rough Infrastructure Estimation for Fast Loans

Based on the rough capacity estimation, here's an infrastructure estimation for our "Fast Loans" application with 1 million users and 1 application per user per day:

**Load Balancer(s)**:

- 1 or more load balancers to distribute the incoming traffic across multiple instances of the Uvicorn server. We may need to scale this horizontally based on the actual request rate and our chosen load balancing solution.

**FastAPI Instances (Uvicorn servers)**:

- Start with 5-10 instances of the Uvicorn server, with each instance running multiple workers (e.g., 4-8 workers). Allocate 2-4 GB RAM per instance. Monitor the CPU and memory usage of these instances and adjust the number of instances or workers as needed to maintain optimal performance.

**Redis Cache**:

- Use 1 or more Redis instances to cache frequently accessed data and reduce the load on the PostgreSQL database. Consider using Redis clustering for improved performance and high availability. Allocate at least 5 GB RAM for caching, considering the size of the dataset and potential growth.

**Kafka Cluster**:

- Use a Kafka cluster with at least 3 brokers for high availability and fault tolerance. Adjust the number of brokers based on the actual message throughput and desired level of redundancy.Allocate 4-8 GB RAM per Kafka broker.

**Kafka Consumers**:

- Start with 5-10 Kafka consumers for processing loan applications. Monitor their performance and scale the number of consumers as needed to maintain optimal processing rates.Allocate 1-2 GB RAM per Kafka Consumer, depending on the number of topics, partitions, and message throughput.

**PostgreSQL Database**:

- Use a PostgreSQL database with at least 1 primary and 1 replica (for high availability) and 30 GB of storage capacity. Monitor the storage usage and scale the storage capacity and number of replicas as needed based on our data retention policy and performance requirements.
- Allocate 8-16 GB RAM for the primary and replica instances. Monitor the database's performance and memory usage, and adjust the RAM allocation as needed.

**Risk Assessment and Loan Approval Modules**:

- Deploy these modules on separate servers or containers, with sufficient CPU and memory resources to handle the expected load. Allocate 2-4 GB RAM per server or container. Monitor their performance and scale them as needed to maintain optimal processing times.

**Error logging and latency monitoring**:

- Use Sentry for error logging and automatic error tracking.
- Integrate Elastic APM for latency monitoring and tracing, which helps us identify performance bottlenecks and optimize our application.

**Deploying**:

- Deploying using Docker and Kubernetes can help manage the scaling, deployment, and orchestration of our application components.
- Create separate Docker images for each component of our application, such as FastAPI, Risk Assessment Module, Loan Approval Module, and Kafka Consumer.
- Use a Kubernetes cluster with at least 3 master nodes and a sufficient number of worker nodes to handle the deployment of application components.


## Requirements

- Python 3.8+
- PostgreSQL
- FastAPI
- Kafka

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/harshkumar742/fast-loans.git
   ```

2. Navigate to the project directory:

   ```
   cd fast-loans
   ```

3. Set up a virtual environment:

   - For Windows:

     ```
     python -m venv venv
     venv\Scripts\activate
     ```

   - For Linux/Mac:

     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

4. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

5. Configure your PostgreSQL database and Kafka broker settings in the `.env` file.

   ```python
   DB_URL = postgresql://username:password@hostname:port/database
   KAFKA_BROKER_URL = your-kafka-broker-url:port
   KAFKA_TOPIC = your-kafka-topic
   KAFKA_SEC_PROTOCOL = your-security-protocol
   KAFKA_SASL_MECH = your-sasl-mechanism
   KAFKA_USERNAME = your-kafka-username
   KAFKA_PASSWORD = your-kafka-password
   ```

6. Apply the database schema:

   ```python
   from app.db.database import engine
   from app.db.models import Base

   Base.metadata.create_all(bind=engine)
   ```

## Running the Application


1. To run the application as a FastAPI server, use one of the following commands:

   ```
   python main.py
   ```

   or

   ```
   uvicorn main:app --workers 4
   ```
   
2. To run the application as a Kafka consumer, use the following command:

   ```
   python main.py --consumer
   ```

## Running Tests

1. Run the tests with pytest:

   ```
   pytest tests/
   ```

## Logging

- Fast Loans uses the Python `logging` module for logging. The logging configuration is set up in the `logging_config.py` file, which defines a `configure_logging` function that sets up a logger with a specific format and level.

- The `configure_logging` function is then called in the main FastAPI application file (`main.py`) and in other files where logging is needed, to set up the logger for that specific module.

- The log messages are written to a file named `app.log`. Each log message includes the timestamp, logger name, severity level, and message text.

## Basic Project Structure

```
fast-loans
├── app
│   ├── api
│   ├── db
│   ├── kafka
│   ├── models
│   ├── loan_approval
│   ├── risk_assessment
    └── logging_config.py
├── tests
├── main.py
└── requirements.txt
```

- `app`: Contains the main components of the application.
  - `api`: RESTful API to expose operations for submitting a new loan application, retrieving the status of a submitted application and updating and deleting an existing application.
  - `db`: Database configuration and models.
  - `kafka`: Kafka producer and consumer implementation.
  - `models`: Pydantic models to validate the data received in API requests .
  - `loan_approval`: Logic for loan approval.
  - `risk_assessment`: Risk assessment for loan applications.
  - `logging_config.py`: Logging configuration.
- `tests`: Contains test files for the application.
- `main.py`: The main entry point of the application.
- `requirements.txt`: Contains the list of required packages for the project.

## API Endpoints

The Fast Loans API exposes the following endpoints:

1. `POST /loan_applications`: Submit a new loan application.
2. `GET /loan_applications/{id}`: Retrieve the status of a submitted loan application by ID.
3. `PATCH /loan_applications/{id}`: Update an existing loan
4. `DELETE /loan_applications/{id}`: Delete an existing loan application by ID.

## Database Model

```python
from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.database import Base

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    applicant_name = Column(String(255))
    credit_score = Column(Integer)
    loan_amount = Column(Float)
    loan_purpose = Column(String(255))
    monthly_income = Column(Float)
    monthly_debt = Column(Float)
    employment_status = Column(String(255))
    risk_score = Column(Integer)
    is_approved = Column(Boolean)
```

## Contribution

Feel free to contribute to this project by submitting issues or creating pull requests. Please follow the standard coding conventions and write test cases for any new features.

## License

This project is licensed under the Apache License, Version 2.0.

## Deployment

You can deploy this application on your preferred platform. Here are some examples of how to deploy the Fast Loans application on popular platforms:

### Heroku

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and log in.

2. Navigate to the project directory:

   ```
   cd fast-loans
   ```

3. Create a new Heroku app:

   ```
   heroku create
   ```

4. Add the Heroku PostgreSQL add-on:

   ```
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. Set the environment variables in the Heroku dashboard based on your `.env` file.

6. Deploy the application:

   ```
   git push heroku master
   ```

7. Scale the web and worker processes:

   ```
   heroku ps:scale web=1
   heroku ps:scale worker=1
   ```

### AWS

1. Set up an [Amazon RDS](https://aws.amazon.com/rds/) PostgreSQL instance.

2. Create an [Amazon MSK](https://aws.amazon.com/msk/) Kafka cluster or use [Confluent Kafka](https://www.confluent.io/get-started/).

3. Deploy the Fast Loans application using [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) or [AWS Lambda](https://aws.amazon.com/lambda/) with [Zappa](https://github.com/Miserlou/Zappa).

4. Update the environment variables in the AWS Management Console based on your `.env` file.

## Support

If you encounter any issues or have any questions, feel free to open an issue on GitHub. We will try our best to help you resolve your problems.

## Acknowledgements

We would like to thank the following projects and libraries for making this project possible:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Kafka](https://kafka.apache.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Authors

- **Harsh Kumar** - *Initial work* - [harshkumar742](https://github.com/harshkumar742)

See also the list of [contributors](https://github.com/yourusername/fast-loans/contributors) who participated in this project.
```
