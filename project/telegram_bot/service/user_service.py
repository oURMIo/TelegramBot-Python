import os
import json
from datetime import datetime
from threading import Lock


class _UserFileService:
    _instance = None
    _lock = Lock()

    def __new__(cls, filename: str = "./telegram_bot/data/user_data.json"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(_UserFileService, cls).__new__(cls)
                cls._instance._init(filename)
            return cls._instance

    def _init(self, filename):
        self.filename = filename
        self.user_data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as json_file:
                return json.load(json_file)
        else:
            return {"users": []}

    def save_user(self, user_id: int, username: str):
        existing_user = next(
            (user for user in self.user_data["users"] if user["userId"] == user_id),
            None,
        )
        if not existing_user:
            time_registered = str(datetime.now())
            user_info = {
                "userId": user_id,
                "username": username,
                "subscribe": False,
                "time_registered": time_registered,
            }
            self.user_data["users"].append(user_info)
            self._save_data()

    def remove_user(self, user_id: int):
        for user in self.user_data["users"]:
            if user["userId"] == user_id:
                self.user_data["users"].remove(user)
                self._save_data()

    def get_users(self):
        return self.user_data["users"]

    def _save_data(self):
        with open(self.filename, "w") as json_file:
            json.dump(self.user_data, json_file)

    def subscribe(self, user_id: int):
        for user in self.user_data["users"]:
            if user["userId"] == user_id:
                user["subscribe"] = True
                self._save_data()
                break

    def unsubscribe(self, user_id: int):
        for user in self.user_data["users"]:
            if user["userId"] == user_id:
                user["subscribe"] = False
                self._save_data()
                break

    def get_subscribe_users(self):
        subscribe_users = [
            user["userId"] for user in self.user_data["users"] if user["subscribe"]
        ]
        return subscribe_users

    def check_user_exists(self, user_id: int):
        return any(user["userId"] == user_id for user in self.user_data["users"])


# Singleton instance of _UserFileService
user_file_service = _UserFileService()


def user_save(user_id: int, user_name: str):
    user_file_service.save_user(user_id=user_id, username=user_name)


def user_subscribe(user_id: int):
    user_file_service.subscribe(user_id=user_id)


def user_unsubscribe(user_id: int):
    user_file_service.unsubscribe(user_id=user_id)


def user_get_all():
    return user_file_service.get_users()


def user_get_subscribe_all():
    return user_file_service.get_subscribe_users()


def user_check_exist(user_id: int):
    return user_file_service.check_user_exists(user_id=user_id)
