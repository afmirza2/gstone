from typing import List
from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.models.loan import Loan
from app.db.mockdb import users
from datetime import datetime


router = APIRouter()


@router.post("", response_model=User)
def create_user(user: User):
    users[user.id] = user
    return user


@router.get("", response_model=List[User])
def get_users():
    return list(users.values())


@router.post("/{user_id}/loans", response_model=Loan)
def create_loan(user_id: str, loan: Loan):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    loan.id = f"{user_id}_{datetime.now().isoformat()}"
    users[user_id].loans.append(loan)
    return loan


@router.get("/{user_id}/loans", response_model=List[Loan])
def user_loans(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id].loans
