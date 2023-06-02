from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.loan import Loan


class User(BaseModel):
    id: str
    loans: Optional[List[Loan]] = []
