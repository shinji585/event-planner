from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid
from typing import Annotated

from schemas.image import ImageOut
from schemas.participation import ParticipationOut


class EventBase(BaseModel):
    title: Annotated[str, Field(min_length=2, max_length=20)]
    description: Annotated[str, Field(min_length=25, max_length=70)]
    event_date: Annotated[datetime, Field(...)]


class EventCreate(EventBase):

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "Reposición: Creatina Monohidrato",
                "description": "Ingreso de 500 unidades. Lote L-992. Verificación de caducidad: 2028-12.",
                "event_date": "2026-04-26T09:00:00",
            }
        },
    )


class EventOut(EventBase):
    id: uuid.UUID
    join_code: Annotated[
        str, Field(min_length=7, max_length=7, pattern=r"^[a-z0-9]{5}$")
    ]

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "join_code": "A9F7K2B",
                "title": "Reposición: Creatina Monohidrato",
                "description": "Ingreso de 500 unidades. Lote L-992. Verificación de caducidad: 2028-12.",
                "event_date": "2026-04-26T09:00:00",
            }
        },
    )


class EventDetail(EventBase):
    id: uuid.UUID
    participants: Annotated[list[ParticipationOut], Field(default_factory=list)]
    images: Annotated[list[ImageOut], Field(default_factory=list)]

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "participants": [
                    {
                        "id": "d290f1ee-e89b-12d3-a456-426614174000",
                        "role": "participant",
                    }
                ],
                "images": [
                    {
                        "id": "e110b2cc-e89b-12d3-a456-426614174000",
                        "url": "https://cdn.performance-log.io/pr.jpg",
                    }
                ],
                "title": "Reposición: Creatina Monohidrato",
                "description": "Ingreso de 500 unidades. Lote L-992. Verificación de caducidad: 2028-12.",
                "event_date": "2026-04-26T09:00:00",
            }
        },
    )
