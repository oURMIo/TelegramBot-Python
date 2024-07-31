import telebot
from telebot import types
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


def _send_message(
    user_id: int,
    message_text: str = "No text",
    reply_markup=types.ReplyKeyboardRemove(),
):
    try:
        bot.send_message(
            user_id,
            message_text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    except Exception as e:
        logging.exception(
            "Can't send a message to user with id:%d %r",
            user_id,
            e,
        )
