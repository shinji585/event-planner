from pydantic import  BaseModel, Field
from datetime import  date
import  uuid

from schemas.image import ImageOut
from schemas.participation import JoinEvent, ParticipationOut


class EventBase(BaseModel):
    title: str = Field(min_length=2,max_length=20)
    description: str = Field(min_length=25,max_length=70)
    event_date: date = Field(...)

class EventCreate(EventBase):
    pass

class EventOut(EventBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    join_code: JoinEvent

class EventDetail(EventBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    participants: list[ParticipationOut] = Field(default_factory=list)
    images: list[ImageOut] = Field(default_factory=list)
