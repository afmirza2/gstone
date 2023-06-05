# Greystone Labs - Coding Challenge

This project is a REST API used for calculated Loan Amoritization. This was developed using FastAPI and SQLAlchemy + SQLite for the database.

Run from the root directory with the command `fastapi run`

## Project Modules

- `core` contains the settings for FastAPI in config.py

- `db` contains the SQLAlchemy settings and database models

- `routers`
   -  `user_router` contains endpoints related to the user
   -  `loan_router` contains loan related endpoints

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
- `GET /loans/{loan_id}/share/{user_id}`

<img width="800" alt="Screenshot 2023-06-04 at 10 57 50 PM" src="https://github.com/afmirza2/gstone/assets/14025552/3aa05d0f-ee23-4641-a8d0-73e1e805ad0d">
