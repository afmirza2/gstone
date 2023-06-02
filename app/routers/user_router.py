from typing import List
from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.db.mockdb import users

router = APIRouter()


@router.post("/user/", response_model=User)
def create_user(user: User):
    users[user.id] = user
    return user


@router.get("/users/", response_model=List[User])
def get_users():
    return list(users.values())
