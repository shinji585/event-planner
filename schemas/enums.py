from enum import  Enum

class Role(str, Enum):
    creator = "creator"
    participant = "participant"