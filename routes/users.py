from uuid import UUID
from typing import  Union
from fastapi import APIRouter, HTTPException, status
from models.users import  UserSignIn, UserOut, UserCreate

user_router = APIRouter(tags=["User"])


# simulate db
users_db: dict[UUID, Union[UserOut, UserCreate]] = {}


@user_router.post("/singnup")
async def sing_new_user(data: UserCreate) -> dict:
    if data.id in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists",
        )
    users_db[data.id] = data
    return {"message": "User successfully registered"}


@user_router.post("/login")
async def sing_user_in(user_data: UserSignIn) -> dict:
    for user in users_db.values():
        if user.email == user_data.email and user.password == user_data.password:
            return {"message": "Login successful"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )

@user_router.post("/out")
async def out_user(data: UserOut) -> dict:
    if data.id in users_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with supplied id exists"
        )
    users_db[data.id] = data
    return {"message": "User successfully registered"}


@user_router.get("/out/{user_id}")
async  def out_user(user_id: UUID)  -> dict:
    if user_id not in users_db:
        raise  HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied id does not exist"
        )
    return {
        "message": users_db[user_id]
    }