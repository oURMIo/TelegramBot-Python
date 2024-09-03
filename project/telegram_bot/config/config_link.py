import configparser
from pathlib import Path
import logging
import os
from config.config_log import setup_logging

# Setup logging
setup_logging()

# Global constants
BCARD_URL = ""
CLUSTER_CHECK_URL_1 = ""
CLUSTER_CHECK_URL_2 = ""
WEBCM_TOOL_URL = ""
WEBCM_PROJECTS_URL = ""
WEBCM_BOT_TOOL_URL = ""


def load_config(file_path: str = "config/link.ini"):
    global BCARD_URL, CLUSTER_CHECK_URL_1, CLUSTER_CHECK_URL_2, WEBCM_TOOL_URL, WEBCM_PROJECTS_URL, WEBCM_BOT_TOOL_URL

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = os.path.join(base_dir, file_path)
    config = configparser.ConfigParser()
    file_path = Path(filename).resolve()

    if not file_path.is_file():
        logging.error(f"Config file not found: {file_path}")
        return

    config.read(file_path)

    BCARD_URL = config.get("BUSINESS_CARD", "BCARD_URL", fallback="")
    CLUSTER_CHECK_URL_1 = config.get("CHECK_CLUSTER", "CLUSTER_URL_1", fallback="")
    CLUSTER_CHECK_URL_2 = config.get("CHECK_CLUSTER", "CLUSTER_URL_2", fallback="")
    WEBCM_TOOL_URL = config.get("WEB_CM", "TOOL_URL", fallback="")
    WEBCM_PROJECTS_URL = config.get("WEB_CM", "PROJECT_URL", fallback="")
    WEBCM_BOT_TOOL_URL = config.get("WEB_CM", "BOT_TOOL_URL", fallback="")


load_config()


def get_bcard_url() -> str:
    return BCARD_URL


def get_cluster_1_check_url() -> str:
    return CLUSTER_CHECK_URL_1


def get_cluster_2_check_url() -> str:
    return CLUSTER_CHECK_URL_2


def get_webcm_tool_url() -> str:
    return WEBCM_TOOL_URL


def get_webcm_project_url() -> str:
    return WEBCM_PROJECTS_URL


def get_webcm_bot_tool_url() -> str:
    return WEBCM_BOT_TOOL_URL
