from fastapi import APIRouter, HTTPException, status
from models.users import UserBase, UserSignIn, UserOut, UserCreate

user_router = APIRouter(tags=["User"])


# simulate db
users: dict = {}


@user_router.post("/singnup")
async def sing_new_user(data: UserCreate) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User witn supplied username exists",
        )
    users[data.email] = data
    return {"message": "User successfully registered"}


@user_router.post("/singin")
async def sing_user_in(user: UserSignIn) -> dict: 
    if users[user.email] not in users: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )
    return {
        "message": "User signed in successfully"
    }