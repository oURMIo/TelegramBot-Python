from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    user_id: int
    username: str
    first_name: str
    last_name: str
    is_subscribe: bool
    time_registered: datetime

    def __post_init__(self):
        if not isinstance(self.user_id, int) or self.user_id <= 0:
            raise ValueError("user_id must be a positive integer")
        if not isinstance(self.username, str) or not self.username.strip():
            raise ValueError("username must be a non-empty string")
        if not isinstance(self.is_subscribe, bool):
            raise ValueError("is_subscribe must be a boolean value")

    def __repr__(self) -> str:
        return (
            f"User(user_id={self.user_id}, username='{self.username}', "
            f"first_name='{self.first_name}', last_name='{self.last_name}', "
            f"is_subscribe={self.is_subscribe}, time_registered='{self.time_registered}')"
        )
