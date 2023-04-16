
# Fast Loans

A simplified, scalable loan approval system that can evaluate loan applications, calculate the risk of lending, and approve or reject applications based on predefined criteria.

## Frontend

A basic frontend for the Fast Loans project is available at the following URL:

[https://main.d221526vcnzerk.amplifyapp.com/](https://main.d221526vcnzerk.amplifyapp.com/)

Visit the link to interact with the loan application system through a web interface.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
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

1. To run the application as a Kafka consumer, use the following command:

   ```
   python main.py --consumer
   ```

2. To run the application as a FastAPI server, use one of the following commands:

   ```
   python main.py
   ```

   or

   ```
   uvicorn main:app
   ```

## Running Tests

1. Run the tests with pytest:

   ```
   pytest tests/
   ```

## Basic Project Structure

```
fast-loans
├── app
│   ├── api
│   ├── db
│   ├── kafka
│   ├── loan_approval
│   └── risk_assessment
├── tests
├── main.py
└── requirements.txt
```

- `app`: Contains the main components of the application.
  - `api`: RESTful API to expose operations for submitting a new loan application, retrieving the status of a submitted application, updating and deleting an existing application and Kafka producer.
  - `db`: Database configuration and models.
  - `kafka`: Kafka consumer implementation.
  - `loan_approval`: Logic for loan approval.
  - `risk_assessment`: Risk assessment for loan applications.
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
