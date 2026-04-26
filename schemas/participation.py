from pydantic import  BaseModel, Field
import  uuid

class ParticipationOut(BaseModel):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    role: Role

class JoinEvent(BaseModel):
    join_code: str = Field(min_length=5,max_length=5)