import json
from pathlib import Path


class BaseRepository:
    def __init__(self, filename: str):
        self.path = Path(__file__).parent.parent / "db_simulated" / filename
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []

        content = self.path.read_text()

        return json.loads(content) if content.strip() else []

    def save(self, data: list[dict]) -> None:
        self.path.write_text(json.dumps(data, indent=4))
