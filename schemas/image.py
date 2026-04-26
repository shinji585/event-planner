import uuid

from pydantic import  Field, AnyUrl, BaseModel

class ImageBase(BaseModel):
    url: AnyUrl

class ImageCreate(ImageBase):
    pass

class ImageOut(ImageBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

