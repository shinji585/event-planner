import uuid
from pathlib import Path
import json


from schemas.user import UserCreate, UserOut


class UserServices:

    BASE_DIR: Path = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "db_simulated"
    USERS_PATH = DB_PATH / "users.json"

    def __load_users(self) -> list[dict]:
        self.USERS_PATH.parent.mkdir(parents=True, exist_ok=True)

        if not self.USERS_PATH.exists():
            return []
        content = self.USERS_PATH.read_text()

        if not content.strip():
            return  []

        return  json.loads(content)

    def __save_users(self,users: list[dict]) -> None:
        self.USERS_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.USERS_PATH.write_text(json.dumps(users, indent=4))

    def create_user(self,**data) -> UserOut:
        # create the instance of user and validate it
        user = UserCreate(**data)

        # convert to dict
        user_data = user.model_dump()

        # generate id
        user_data["id"] = str(uuid.uuid4())
        user_data["email"] = user_data["email"].lower()

        users = self.__load_users()

        for existing_user in users:
            if existing_user["email"] == user_data["email"]:
                raise ValueError("Email already registered")

        # append the new user
        users.append(user_data)
        self.__save_users(users)

        return  UserOut.model_validate(user_data)

    def get_user_by_id(self, id_user: str) -> UserOut:
        users = self.__load_users()

        user = next(
            (u for u in users if u["id"] == id_user),
            None
        )

        if user is None:
            raise LookupError("User not found")

        return  UserOut.model_validate(user)

    def get_user_by_email(self,email_user: str) -> UserOut:
        users = self.__load_users()
        email_user = email_user.lower()

        user = next(
            (u for u in users if u["email"] == email_user),
            None
        )

        if user is None:
            raise  LookupError("User not found")

        return  UserOut.model_validate(user)

    def authenticate_user(self,email_user: str, password_user: str) -> UserOut:
        users = self.__load_users()
        email_user = email_user.lower()

        user = next((u for u in users if u["email"] == email_user), None)

        if user is None:
            raise LookupError("User not found")

        if user["password"] != password_user:
            raise ValueError("Invalid credentials")

        return UserOut.model_validate(user)

    def get_all_users(self) -> list[UserOut]:
        users = self.__load_users()
        return  [UserOut.model_validate(u) for u in users]