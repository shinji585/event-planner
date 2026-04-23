import uuid

from pydantic import BaseModel, EmailStr, Field
from models.events import Event


class UserBase(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: EmailStr
    username: str = Field(..., min_length=1, max_length=20)

    model_config = {
        "json_schema_extra": {
            "example": {"username": "Francisco", "email": "fastapi@packt.com"}
        }
    }


class PasswordMixin(BaseModel):
    password: str = Field(..., min_length=8, max_length=50)

    model_config = {"json_schema_extra": {"example": {"password": "strongpassword"}}}


class UserCreate(UserBase, PasswordMixin):
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "Francisco",
                "email": "fastapi@packt.com",
                "password": "strongpassword",
            }
        }
    }


class UserSignIn(PasswordMixin):
    email: EmailStr = Field(...)

    model_config = {
        "json_schema_extra": {
            "example": {"email": "fastapi@packt.com", "password": "strongpassword"}
        }
    }


class UserOut(UserBase):
    events: list[Event] = Field(default_factory=list)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "Francisco",
                "email": "fastapi@packt.com",
                "events": [],
            }
        }
    }