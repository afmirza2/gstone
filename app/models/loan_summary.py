from pydantic import BaseModel


class LoanSummary(BaseModel):
    current_principal_balance: float
    principal_paid: float
    interest_paid: float
