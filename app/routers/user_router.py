import uuid
from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import models
from app.schemas.user import User
from app.schemas.loan import Loan, LoanCreate
from app.db.sqldb import get_db


router = APIRouter()


@router.post("", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.id == user.id).first()
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = models.User(id=user.id, loans=user.loans)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/{user_id}/loans", response_model=List[Loan])
def user_loans(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.loans


@router.post("/{user_id}/loans", response_model=Loan)
def create_loan(user_id: str, loan: LoanCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    loan_id = str(uuid.uuid4())
    created_loan = Loan(amount=loan.amount, annual_interest_rate=loan.annual_interest_rate,
                        loan_term_in_months=loan.loan_term_in_months, id=loan_id)

    db_loan = models.Loan(id=loan_id, amount=loan.amount, annual_interest_rate=loan.annual_interest_rate,
                          loan_term_in_months=loan.loan_term_in_months, user_id=user_id, user=user)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return created_loan
