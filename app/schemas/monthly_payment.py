from pydantic import BaseModel


class MonthlyPayment(BaseModel):
    month: int
    remaining_balance: float
    monthly_payment: float
