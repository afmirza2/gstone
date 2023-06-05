from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from app.db import models
from app.schemas.user import User
from app.schemas.loan import Loan
from app.db.sqldb import get_db
from sqlalchemy.orm import Session
from app.schemas.monthly_payment import MonthlyPayment
from app.schemas.loan_summary import LoanSummary
from app.db.mockdb import users
from app.services.loan_service import amortization_schedule


router = APIRouter()


@router.get("/{loan_id}/schedule", response_model=List[MonthlyPayment])
def loan_schedule(loan_id: str, db: Session = Depends(get_db)):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return amortization_schedule(loan)


@router.get("/{loan_id}/summary/{month}", response_model=LoanSummary)
def loan_summary(loan_id: str, month: int, db: Session = Depends(get_db)):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    schedule = amortization_schedule(loan)

    if month < 0 or month > len(schedule):
        raise HTTPException(
            status_code=400, detail="Invalid month number")
    month_info = schedule[month - 1]
    principal_paid = loan.amount - \
        float(month_info["remaining_balance"])
    interest_paid = float(month_info["monthly_payment"]) * \
        month - principal_paid
    return LoanSummary(current_principal_balance=month_info["remaining_balance"],
                       principal_paid=round(principal_paid, 2),
                       interest_paid=round(interest_paid, 2))


@router.post("/{loan_id}/share/{user_id}", response_model=Dict[str, str])
def share_loan(loan_id: str, user_id: str, db: Session = Depends(get_db)):
    loan = db.query(models.Loan).get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if loan not in user.loans:
        user.loans.append(loan)
        db.commit()

    return {"detail": f"Loan {loan_id} shared with user {user_id}"}
