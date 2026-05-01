from pydantic import  BaseModel, Field, ConfigDict
import  uuid
from typing import  Annotated
from schemas.enums import Role


class ParticipationBase(BaseModel):
    user_id: uuid.UUID
    role: Role

class ParticipationOut(ParticipationBase):

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_schema_extra={
            "examples": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "creator"
            }
        }
    )

class JoinEvent(BaseModel):
    join_code: Annotated[str, Field(min_length=7,max_length=7)]

    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            "example": {
                "join_code": "A9F7K2B"
            }
        }
    )