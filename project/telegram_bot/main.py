import telebot
import logging
from config.log_config import setup_logging, start_scheduler
from config.bot_config import bot
from service.bot_main_service import init_bot_service
from service.demon_service import init_demons

# Setup logging
setup_logging()
start_scheduler()

init_bot_service()
init_demons()


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except telebot.apihelper.ApiException as e:
        logging.exception("Telegram API Error: %r", e)
    except Exception as e:
        logging.exception("Error occurred while polling: %r", e)
