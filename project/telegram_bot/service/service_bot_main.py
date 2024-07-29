from telebot import types
import logging
from service.service_user import user_save, user_check_exist
from config.config_logging import setup_logging
from config.config_bot import bot

# Setup logging
setup_logging()


@bot.message_handler(commands=["help"])
def handle_help_message(message):
    # TODO finish this method
    if check_user_exist(user_id=message.from_user.id):
        _send_message(
            user_id=message.from_user.id,
            message_text=f"""TODO""",
        )


@bot.message_handler(commands=["start"])
def handle_start_message(message):
    name = message.from_user.first_name
    logging.info("Got new user %s with ID:'%d'", name, message.from_user.id)
    user_save(user_id=message.from_user.id, user_name=name)
    _send_message(
        user_id=message.from_user.id,
        message_text=f"""Greetings, {name}
I am Sagiri, your humble assistant bot.
I am here to assist you by diligently checking the status of our servers and promptly notifying you of their condition""",
    )


@bot.message_handler(content_types=["text"])
def handle_text_message(message):
    if check_user_exist(user_id=message.from_user.id):
        _send_message(
            user_id=message.from_user.id,
            message_text="I do not understand you. Select a function from the given list /help",
        )


def check_user_exist(user_id: int):
    if not user_check_exist(user_id=user_id):
        _send_message(
            user_id=user_id,
            message_text="Excuse me, Sir/Madam, might I kindly request that you use the '/start' command from the very beginning?",
        )
        return False
    return True


def _send_message(user_id: int, message_text: str):
    try:
        bot.send_message(
            user_id,
            message_text,
            reply_markup=types.ReplyKeyboardRemove(),
        )
    except Exception as e:
        logging.exception(
            "Can't send a message to user with id:%d %r",
            user_id,
            e,
        )
