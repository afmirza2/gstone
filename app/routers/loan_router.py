from typing import List
from fastapi import APIRouter, HTTPException
from app.models.monthly_payment import MonthlyPayment
from app.models.loan_summary import LoanSummary
from app.db.mockdb import users
from app.services.loan_service import amortization_schedule

router = APIRouter()


@router.get("/{loan_id}/schedule", response_model=List[MonthlyPayment])
def loan_schedule(loan_id: str):
    for user in users.values():
        for loan in user.loans:
            if loan.id == loan_id:
                return amortization_schedule(loan)
    raise HTTPException(status_code=404, detail="Loan not found")


@router.get("/{loan_id}/summary/{month}", response_model=LoanSummary)
def loan_summary(loan_id: str, month: int):
    for user in users.values():
        for loan in user.loans:
            if loan.id == loan_id:
                schedule = amortization_schedule(loan)
                if month > len(schedule):
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
    raise HTTPException(status_code=404, detail="Loan not found")
