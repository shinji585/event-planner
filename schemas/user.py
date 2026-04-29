import uuid
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserBase(BaseModel):
    name: Annotated[
        str, Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9 ]+$")
    ]
    email: EmailStr

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        from_attributes=True,
        json_schema_extra={
            "examples": {
                    "name": "Francisco",
                    "email": "fastapi@packt.com"
            }
        }
    )


class Password(BaseModel):
    password: Annotated[str, Field(min_length=8, max_length=30)]

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        str_strip_whitespace=False,
        json_schema_extra={
            "examples": {
                    "password": "secret_password123"
            }
        }
    )


class UserCreate(UserBase, Password):
    phone: PhoneNumber
    id: uuid.UUID

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_schema_extra={
            "examples": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Francisco",
                    "email": "fastapi@packt.com",
                    "password": "secret_password123",
                    "phone": "3234286431"
            }
        }
    )


class UserLogin(Password):
    email: EmailStr

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_schema_extra={
            "examples": {
                    "email": "fastapi@packt.com",
                    "password": "secret_password123"
            }
        }
    )


class UserOut(UserBase):
    id: uuid.UUID

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_schema_extra={
            "example": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Francisco",
                    "email": "fastapi@packt.com",
            }
        }
    )