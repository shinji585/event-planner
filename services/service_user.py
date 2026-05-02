import uuid

from database.repository import BaseRepository
from schemas.user import UserCreate, UserOut


class UserServices:
    def __init__(self):
        self.repo = BaseRepository("users.json")

    def create_user(self, **data) -> UserOut:
        # create the instance of user and validate it
        user = UserCreate(**data)

        # convert to dict
        user_data = user.model_dump()

        # generate id
        user_data["id"] = str(uuid.uuid4())
        user_data["email"] = user_data["email"].lower()

        users = self.repo.load()

        for existing_user in users:
            if existing_user["email"] == user_data["email"]:
                raise ValueError("Email already registered")

        # append the new user
        users.append(user_data)
        self.repo.save(users)

        return UserOut.model_validate(user_data)

    def get_user_by_id(self, id_user: str) -> UserOut:
        users = self.repo.load()

        user = next((u for u in users if u["id"] == id_user), None)

        if user is None:
            raise LookupError("User not found")

        return UserOut.model_validate(user)

    def get_user_by_email(self, email_user: str) -> UserOut:
        users = self.repo.load()
        email_user = email_user.lower()

        user = next((u for u in users if u["email"] == email_user), None)

        if user is None:
            raise LookupError("User not found")

        return UserOut.model_validate(user)

    def authenticate_user(self, email_user: str, password_user: str) -> UserOut:
        users = self.repo.load()
        email_user = email_user.lower()

        user = next((u for u in users if u["email"] == email_user), None)

        if user is None:
            raise LookupError("User not found")

        if user["password"] != password_user:
            raise ValueError("Invalid credentials")

        return UserOut.model_validate(user)

    def get_all_users(self) -> list[UserOut]:
        users = self.repo.load()
        return [UserOut.model_validate(u) for u in users]
