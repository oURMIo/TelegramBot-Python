import configparser
from pathlib import Path
import logging
import os
import sys
from config.config_log import setup_logging

# Setup logging
setup_logging()

# Global constants
BOT_TOKEN = ""
MAIN_ADMIN_ID = 0


def _load_config(file_path: str = "config/config.ini"):
    global BOT_TOKEN, MAIN_ADMIN_ID

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = os.path.join(base_dir, file_path)
    config = configparser.ConfigParser()
    file_path = Path(filename).resolve()

    if not file_path.is_file():
        logging.error(f"Config file not found: {file_path}")
        return

    config.read(file_path)

    BOT_TOKEN = config.get("TOKEN", "BOT_TOKEN", fallback="")
    try:
        MAIN_ADMIN_ID = int(config.get("ADMIN_ID", "MAIN_ADMIN_ID", fallback=0))
    except (ValueError, TypeError):
        logging.error(f"Invalid MAIN_ADMIN_ID value. Defaulting to 0.")
        MAIN_ADMIN_ID = 0


_load_config()


def get_bot_token() -> str:
    return BOT_TOKEN


def get_main_admin_id() -> int:
    return MAIN_ADMIN_ID