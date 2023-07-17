# Backend Credit Card

This is a CRUD API for credit cards. Some business rules have been applied:

- **exp_date**
  -- Check if it is a valid date.
  -- If valid, it cannot be less than "today's" date.
  -- In the database, this date should be recorded in the format yyyy-MM-[last_day_of_month], for example: 02/2022, should be 2022-02-28
- **holder**
  -- It should be a required field and must have more than 2 characters.
- **number**
  -- Check if the credit card number is valid, using the lib [https://github.com/MaisTodos/python-creditcard](https://github.com/MaisTodos/python-creditcard)
  -- To install, use `pip install git+https://github.com/maistodos/python-creditcard.git@main`
  -- This field should be stored in an encrypted way in the database.
- **cvv**
  -- This field is not required, but if present in the payload, it must have a length between 3 and 4 characters.
  -- This is a numeric field.

## Stack

| Tool     | Reason                                                                                                                                              |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python   | Programming language with high readability and not verbose: helps in the maintenance and creation of codes with few lines and greater productivity. |
| FastApi  | Framework for creating APIs, automated documentation, and pydantic schema validation                                                                |
| Postgres | Database                                                                                                                                            |
| Alembic  | Tool that abstracts greater complexities for creating migrations                                                                                    |
| Pytest   | Python unit testing framework                                                                                                                       |
| Locust   | Python load testing framework                                                                                                                       |

## How to run the application

### Requirements for execution:

1. Docker/docker-compose
2. Renomeie o arquivo ".env.example" para ".env"

### Steps for execution

1.  `git clone https://github.com/apenasweber/backend-python-creditcard`
2.  `cd backend-python-creditcard`
3.  Rename the `".env-example"` file to `".env"`
4.  `docker-compose up --build`
5.  Access [http://localhost:8000/docs](http://localhost:8000/docs)
6.  Click on /login endpoint, Try it out, insert username(username) and password(password), finally click on execute.
7.  You gonna receive a token: copy it, click on the "Authorize" button on right top of page and paste the token there clicking in Authorize.
8.  Now you can use all endpoints authenticated(20 minutes time expiration for token)

The application can also be run using make, with the following commands and helpers:
|Tool | Reason
|----------------|-------------------------------|
| `make build` | Builds the application and applies alembic migrations |
| `make run` | Runs only the API container|
| `make up` | Runs the whole application (API, database, and coinbase_feeder)|
| `make down` | Takes down the application|
| `make bash` | Accesses the bash terminal of the API container|
| `make unit_tests`| Executes unit tests |
| `make isort` | Applies isort throughout the repository to sort imports |
| `make black` | Applies the black linter |

## Testes

To execute them, use in the terminal, at the project root:

### 1. Unit Tests

```bash
docker compose run --service-ports -e --rm api bash -c "pytest ${test} --disable-warnings
```

### 2. Stress Tests

```bash
docker-compose up -d
```

```bash
docker ps
```

Now copy the API container id

```bash
docker exec -it {container_id da api} bash
```

```bash
locust -f app/tests/stress_tests/locustfile.py --headless -u 1000 -r 17 --run-time 1m --host http://127.0.0.1:8000
```

Note: Load test results may vary or fail depending on your firewall, connection quality, among other factors.

## Database

The database has 2 tables:

- alembic_version: versions of Alembic migrations.
- credit_cards: data of our credit cards in the endpoint `'/credit-card'` [GET]

## Endpoints

The extensive documentation of all kinds of input and output can be found at [https://localhost/8000/docs](https://localhost/8000/docs) as indicated on how to run the application.

| Endpoint                        | Método | Retorno                                      |
| ------------------------------- | ------ | -------------------------------------------- |
| `/api/v1/login`                 | POST   | Performs user login and returns access token |
| `/api/v1/credit-card`           | POST   | Creates a new credit card                    |
| `/api/v1/credit-card`           | GET    | Returns all registered credit cards          |
| `/api/v1/credit-card/{card_id}` | GET    | Returns details of a specific credit card    |
| `/api/v1/credit-card/{card_id}` | DELETE | Deletes a specific credit card               |
| `/api/v1/credit-card/{card_id}` | PUT    | Updates details of a specific credit card    |

Please replace `{card_id}` with the ID of the credit card you want to get, delete, or update."
