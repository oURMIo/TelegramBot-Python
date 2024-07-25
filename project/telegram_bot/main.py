import telebot
from telebot import types
import logging
from config.config_logging import setup_logging
from config.config_bot import bot


# Setup logging
setup_logging()


if not bot.token:
    logging.error("Bot token not found. Make sure to provide a valid token.")
    exit()


@bot.message_handler(content_types=["text"])
def responsi_text_message(message):
    try:
        bot.send_message(
            message.from_user.id,
            "I do not understand you. Select a function from the given list /help",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    except Exception as e:
        logging.exception(
            "Can't send a message to user name:%r,id:%d %r",
            message.from_user.first_name,
            message.from_user.id,
            e,
        )


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except telebot.apihelper.ApiException as e:
        logging.exception("Telegram API Error: %r", e)
    except Exception as e:
        logging.exception("Error occurred while polling: %r", e)
