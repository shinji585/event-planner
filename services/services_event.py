import json
import string
import uuid
from datetime import datetime
from pathlib import Path
from random import choices
from typing import Optional


from schemas.enums import Role
from schemas.event import EventCreate, EventDetail, EventOut
from schemas.image import ImageCreate
from schemas.participation import ParticipationBase


class EventServices:

    BASE_DIR: Path = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "db_simulated"
    EVENTS_PATH = DB_PATH / "events.json"

    def __load_events(self) -> list[dict]:

        self.EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)

        if not self.EVENTS_PATH.exists():
            return []

        content = self.EVENTS_PATH.read_text()

        if not content.strip():
            return []

        return json.loads(content)

    def __save_events(self,
                      events: list[dict]) -> None:

        self.EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.EVENTS_PATH.write_text(json.dumps(events, indent=4))

    @staticmethod
    def __generate_code(length=7) -> str:

        characters = string.ascii_uppercase + string.digits
        return "".join(choices(characters, k=length))

    @staticmethod
    def __find_event(events: list[dict],reference_id: str) -> dict:
        for event in events:
            if event["id"] == reference_id:
                return  event

        raise LookupError("Id is not on db")

    @staticmethod
    def __find_event_by_code(events: list[dict], reference_id: str) -> dict:
        for event in events:
            if event["join_code"] == reference_id:
                return  event

        raise  LookupError("join code is not on db")

    def create_event(self,
                     creator_id: str,
                     users_id: Optional[list[str]] = None,
                     **data) -> EventOut:

        event = EventCreate(**data)

        event_data = event.model_dump()

        event_data["id"] = str(uuid.uuid4())
        creator_participant = ParticipationBase(user_id=uuid.UUID(creator_id), role=Role.creator)
        event_data["participants"] = [
            creator_participant.model_dump()
        ]

        # check if users_id is not None
        participants: list[dict] = [creator_participant.model_dump()]
        if users_id is not None:
            for user_id in users_id:
                user_participant = ParticipationBase(user_id=uuid.UUID(user_id), role=Role.participant)
                participants.append(user_participant.model_dump())
                event_data["participants"] = participants

        # generate join code
        event_data["join_code"] = self.__generate_code()

        # generate the list of image empty
        event_data["images"] = []

        events = self.__load_events()

        # append the new event
        events.append(event_data)
        self.__save_events(events)

        # return the data
        return  EventOut.model_validate(event_data)


    def get_event_by_id(self, event_id: str) -> EventOut:
        events = self.__load_events()

        event = next(
            (e for e in events if e["id"] == event_id),
            None
        )

        if event is None:
            raise  LookupError("Event not found")

        return  EventOut.model_validate(event)

    def get_all_events(self) -> list[EventOut]:
        events = self.__load_events()
        return  [EventOut.model_validate(e) for e in events]

    def update_event(self,
                     event_id: str,
                     title: Optional[str] = None,
                     description: Optional[str] = None,
                     event_date: Optional[datetime] = None) -> EventOut:

        events = self.__load_events()
        event = self.__find_event(events=events, reference_id=event_id)

        if title is not None:
            event["title"] = title

        if description is not None:
            event["description"] = description

        if event_date is not None:
            event["event_date"] = event_date

        validated = EventOut.model_validate(event)

        # persistence data
        self.__save_events(events)
        return  validated

    def remove_event(self, event_id: str) -> None:
        events = self.__load_events()
        event = self.__find_event(events=events,reference_id=event_id)

        events.remove(event)
        self.__save_events(events)

    def join_event(self,user_id: str, join_code: str) -> EventDetail:
        events = self.__load_events()
        event = self.__find_event_by_code(events=events, reference_id=join_code)

        for participant in event["participants"]:
            if str(participant["user_id"]) == user_id:
                raise  ValueError("Participant is already joined")

        event["participants"].append(ParticipationBase(user_id=uuid.UUID(user_id), role=Role.participant).model_dump())

        # update the persistence
        self.__save_events(events)

        return  EventDetail.model_validate(event)

    def leave_event(self, user_id: str, event_id: str) -> EventDetail:
        events = self.__load_events()
        event = self.__find_event(events, reference_id=event_id)


        participant_to_remove = next(
            (p for p in event["participants"] if str(p["user_id"]) == user_id),
            None
        )

        if participant_to_remove is None:
            raise  LookupError("Participant not found")

        if participant_to_remove["role"] == Role.creator.value:
            raise  LookupError("Creator cannot leave event")

        event["participants"].remove(participant_to_remove)
        self.__save_events(events)
        return  EventDetail.model_validate(event)

    def get_event_detail(self, event_id: str) -> EventDetail:
        events = self.__load_events()
        event = self.__find_event(events, reference_id=event_id)
        return  EventDetail.model_validate(event)

    def get_event_by_user(self, user_id: str) -> EventDetail:
        events = self.__load_events()

        event = next(
            (
                e for e in events
                if any(str(p["user_id"]) == user_id for p in e["participants"])
            ),
            None
        )

        if event is None:
            raise  LookupError("Participant not found in any event")

        return EventDetail.model_validate(event)

    def add_event_image(self, url: str, event_id: str) -> EventDetail:
        events = self.__load_events()
        event = self.__find_event(events, reference_id=event_id)
        image = ImageCreate(url= url)

        image_data = image.model_dump()
        image_data["id"] = str(uuid.uuid4())

        event["images"].append(image_data)

        validated = EventDetail.model_validate(event)
        self.__save_events(events)

        return  validated