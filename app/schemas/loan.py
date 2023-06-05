from pydantic import BaseModel, Field
from typing import Optional


class LoanCreate(BaseModel):
    amount: float = Field(..., gt=0)
    annual_interest_rate: float = Field(..., gt=0)
    loan_term_in_months: int = Field(..., gt=0)


class Loan(LoanCreate):
    id: Optional[str] = None

    class Config:
        orm_mode = True
