from fastapi import APIRouter

from schemas.user import UserOut

users_db: list[UserOut]


user_router = APIRouter(
    tags=["User"]
)
