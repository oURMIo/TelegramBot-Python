import os
import json
from datetime import datetime
from threading import Lock
import logging
from typing import Dict

from config.config_log import setup_logging
from model.dto_user import User

setup_logging()


class _UserCache:
    _instance = None
    _lock = Lock()

    def __new__(cls, filename: str = "data/user_data.json"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(_UserCache, cls).__new__(cls)
                cls._instance._init(filename)
            return cls._instance

    def _init(self, filename):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filename = os.path.join(base_dir, filename)
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.user_cache: Dict[int, User] = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as json_file:
                data = json.load(json_file)
                return {user['user_id']: User(
                    user_id=user['user_id'],
                    username=user['username'],
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    is_subscribe=user['is_subscribe'],
                    time_registered=datetime.fromisoformat(user['time_registered'])
                ) for user in data.get("users", [])}
        else:
            return {}

    def save_user(self, user_id: int, username: str, first_name: str, last_name: str):
        if user_id not in self.user_cache:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_subscribe=False,
                time_registered=datetime.now()
            )
            self.user_cache[user_id] = user
            self._save_data()

    def remove_user(self, user_id: int):
        if user_id in self.user_cache:
            del self.user_cache[user_id]
            self._save_data()

    def get_user(self, user_id: int) -> User:
        user = self.user_cache.get(user_id)
        if user is None:
            raise KeyError(f"User with ID {user_id} does not exist.")
        return user

    def get_users(self) -> Dict[int, User]:
        return self.user_cache

    def subscribe(self, user_id: int):
        if user_id in self.user_cache:
            self.user_cache[user_id].is_subscribe = True
            self._save_data()

    def unsubscribe(self, user_id: int):
        if user_id in self.user_cache:
            self.user_cache[user_id].is_subscribe = False
            self._save_data()

    def get_subscribe_users(self) -> list:
        return [user_id for user_id, user in self.user_cache.items() if user.is_subscribe]

    def check_user_exists(self, user_id: int) -> bool:
        return user_id in self.user_cache

    def clean_up_all(self):
        self.user_cache.clear()
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def _save_data(self):
        with open(self.filename, "w") as json_file:
            json.dump({
                "users": [
                    {
                        "user_id": user.user_id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "is_subscribe": user.is_subscribe,
                        "time_registered": user.time_registered.isoformat()
                    }
                    for user in self.user_cache.values()
                ]
            }, json_file, default=str)


# Singleton instance of _UserCache
user_cache = _UserCache()


def crete_user(user_id: int, username: str, first_name: str, last_name: str):
    user_cache.save_user(user_id=user_id, username=username, first_name=first_name, last_name=last_name)


def subscribe_user(user_id: int):
    user_cache.subscribe(user_id=user_id)


def unsubscribe_user(user_id: int):
    user_cache.unsubscribe(user_id=user_id)


def get_user(user_id: int) -> User:
    return user_cache.get_user(user_id)


def get_users() -> Dict[int, User]:
    return user_cache.get_users()


def get_subscribe_all_users() -> list:
    return user_cache.get_subscribe_users()


def check_exist_user(user_id: int) -> bool:
    return user_cache.check_user_exists(user_id=user_id)


def clean_cache_user():
    user_cache.clean_up_all()
