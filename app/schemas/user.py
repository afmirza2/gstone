from pydantic import BaseModel
from typing import Optional, List
from app.schemas.loan import Loan


class User(BaseModel):
    id: str
    loans: Optional[List[Loan]] = []

    class Config:
        orm_mode = True
