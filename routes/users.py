from fastapi import  APIRouter,status,HTTPException

from schemas.user import  UserCreate, UserLogin, UserOut

users_db: list[UserOut]


user_router = APIRouter(
    tags=["User"]
)


@user_router.post("/users")
async def create_user(user: UserCreate) -> UserOut:
    pass