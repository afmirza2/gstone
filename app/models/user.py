from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: str
