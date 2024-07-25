import telebot
import logging
from config.config_logging import setup_logging
from service.config_service import get_bot_token

# Setup logging
setup_logging()

TOKEN = get_bot_token()

if not TOKEN or TOKEN == "":
    logging.error("Bot token not found. Make sure to provide a valid token.")
    exit()
else:
    logging.info("Bot token has been received")

bot = telebot.TeleBot(TOKEN)
