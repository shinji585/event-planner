from pydantic import BaseModel, Field
import uuid


class Event(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(..., min_length=5, max_length=100)
    image: str = Field(..., pattern=r"^(http|https)://.*\.(jpg|jpeg|png|gif)$")
    description: str = Field(..., max_length=200)
    tags: list[str] = Field(..., min_length=1)
    location: str = Field(..., min_length=5, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "FASTAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FASTAPI book in this event. Ensure to come with your own copy to win gifts and prizes.",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet",
            }
        }
    }
