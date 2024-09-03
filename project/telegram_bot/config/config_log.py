import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import sched
import shutil
import time
import threading
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(base_dir, "logs/")
MAX_LOG_SIZE = 100 * 1024 * 1024  # 100 MB
LOG_FILE = os.path.join(LOG_DIR, "console.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
COPY_INTERVAL = 12 * 60 * 60  # 12 h


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    open(LOG_FILE, "w").close()
    open(ERROR_LOG_FILE, "w").close()

    logger = logging.getLogger()

    if not logger.handlers:
        # Main log handler
        main_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=1
        )
        main_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(name)s] [%(levelname)s] - [%(message)s]"
            )
        )
        main_handler.encoding = "utf-8"

        # Error log handler
        error_handler = RotatingFileHandler(
            ERROR_LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=1
        )
        error_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(name)s] [%(levelname)s] - [%(message)s]"
            )
        )
        error_handler.encoding = "utf-8"
        error_handler.setLevel(logging.ERROR)

        logger = logging.getLogger()
        logger.addHandler(main_handler)
        logger.addHandler(error_handler)
        logger.setLevel(logging.DEBUG)


def _copy_logs():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    try:
        if os.path.getsize(LOG_FILE) > 0:
            dest_log_file = os.path.join(LOG_DIR, f"console_{timestamp}.log")
            shutil.copy2(LOG_FILE, dest_log_file)
            logging.info(f"Log copied to {dest_log_file}")

        if os.path.getsize(ERROR_LOG_FILE) > 0:
            dest_error_log_file = os.path.join(LOG_DIR, f"error_{timestamp}.log")
            shutil.copy2(ERROR_LOG_FILE, dest_error_log_file)
            logging.info(f"Error log copied to {dest_error_log_file}")
    except Exception as e:
        logging.error(f"Failed to copy logs: {e}")


def _schedule_log_copy(scheduler):
    scheduler.enter(COPY_INTERVAL, 1, _schedule_log_copy, (scheduler,))
    _copy_logs()


def _start_scheduler():
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(COPY_INTERVAL, 1, _schedule_log_copy, (scheduler,))
    threading.Thread(target=scheduler.run, daemon=True).start()
