import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "./telegram_bot/logs/"
MAX_LOG_SIZE = 100 * 1024 * 1024  # 100 MB
LOG_FILE = os.path.join(LOG_DIR, "console.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    open(LOG_FILE, "w").close()
    open(ERROR_LOG_FILE, "w").close()

    # Main log handler
    main_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=1)
    main_handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] - [%(message)s]")
    )
    main_handler.encoding = "utf-8"

    # Error log handler
    error_handler = RotatingFileHandler(
        ERROR_LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=1
    )
    error_handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] - [%(message)s]")
    )
    error_handler.encoding = "utf-8"
    error_handler.setLevel(logging.ERROR)

    logger = logging.getLogger()
    logger.addHandler(main_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.DEBUG)
