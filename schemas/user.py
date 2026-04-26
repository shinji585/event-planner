import  uuid

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import  PhoneNumber

class UserBase(BaseModel):
    name: str  = Field(..., min_length=3, max_length=20,pattern=r"[a-zA-Z0-9]+$")
    email: EmailStr

class Password(BaseModel):
    password: str = Field(min_length=8,max_length=30)

class UserCreate(UserBase,Password):
    phone: PhoneNumber

class UserLogin(Password):
    email: EmailStr

class UserOut(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)