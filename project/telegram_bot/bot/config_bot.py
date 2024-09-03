import telebot
import logging

from config.config_log import setup_logging
from config.config_bot import get_bot_token

setup_logging()

TOKEN = get_bot_token()

if not TOKEN or TOKEN == "":
    logging.error("Bot token not found. Make sure to provide a valid token.")
    exit(1)
else:
    logging.info("Bot token has been received")

bot = telebot.TeleBot(TOKEN)
