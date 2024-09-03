import logging
import telebot
from config.config_log import setup_logging
from config.config_initer import main_initialization
from bot.config_bot import bot

setup_logging()
main_initialization()

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
        logging.info("Bot has been initialized successfully.")
    except telebot.apihelper.ApiException as e:
        logging.exception("Telegram API Error: %r", e)
    except Exception as e:
        logging.exception("Error occurred while polling: %r", e)
