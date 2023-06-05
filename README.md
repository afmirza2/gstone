# Greystone Labs - Coding Challenge

This project is a REST API used for calculated Loan Amoritization. This was developed using FastAPI and SQLAlchemy + SQLite for the database.

To run:
- Rename `.env_template` to `.env`
- Run from the root directory with the command `fastapi run`

## Project Modules

- `core` contains the settings for FastAPI in `config.py`

- `db` contains the SQLAlchemy settings and database models

- `routers`
   -  `user_router` contains endpoints related to users
   -  `loan_router` contains endpoints related to loans

- `schemas` contains pydantic models for `User`, `Loan`, `LoanSummary` and `MonthlyPayment`

- `services` contains the loan amoritization function

## Endpoints

### User
- `GET /users`
- `POST /users`
- `GET /users/{user_id}/loans`
- `POST /users/{user_id}/loans`

### Loan
- `GET /loans/{loan_id}/schedule`
- `GET /loans/{loan_id}/summary/{month}`
- `POST /loans/{loan_id}/share/{user_id}`
