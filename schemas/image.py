import uuid

from pydantic import  AnyUrl, BaseModel, ConfigDict


class ImageBase(BaseModel):
    url: AnyUrl


class ImageCreate(ImageBase):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_schema_extra={"example": {"url": "https://www.jetbrains.com/academy"}},
    )


class ImageOut(ImageBase):
    id: uuid.UUID

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_schema_extra={
            "examples": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "url": "https://www.jetbrains.com/academy",
            }
        },
    )
