from telebot import types
import logging
from config.log_config import setup_logging
from config.link_config import get_bcard_url
from config.bot_config import bot, _send_message
from utils.cluster_util import check_cluster_1_status, check_cluster_2_status
from service.user_service import (
    user_save,
    user_check_exist,
    user_subscribe,
    user_unsubscribe,
)
from service.callback_service import (
    call_cluster_status,
    call_useful_urls,
    call_notifications,
    call_domains,
    call_projects,
)

# Setup logging
setup_logging()


# CHECK STATUS
@bot.message_handler(commands=["check_cluster_dach"])
def handle_help_message(message):
    if check_user_exist(user_id=message.from_user.id):
        message_text = ""
        if check_cluster_1_status():
            message_text = "Dach cluster status is 'WORKING'"
        else:
            message_text = "Dach cluster status is 'SHUTDOWN'"
        _send_message(
            user_id=message.from_user.id,
            message_text=message_text,
        )


@bot.message_handler(commands=["check_cluster_chserv"])
def handle_help_message(message):
    if check_user_exist(user_id=message.from_user.id):
        message_text = ""
        if check_cluster_2_status():
            message_text = "Chserv cluster status is 'WORKING'"
        else:
            message_text = "Chserv cluster status is 'SHUTDOWN'"
        _send_message(
            user_id=message.from_user.id,
            message_text=message_text,
        )


# SUB & UNSUB
@bot.message_handler(commands=["sub_notif"])
def handle_help_message(message):
    if check_user_exist(user_id=message.from_user.id):
        user_subscribe(message.from_user.id)
        _send_message(
            user_id=message.from_user.id,
            message_text="Congratulations, you have successfully subscribed. Now you will receive important notifications",
        )


@bot.message_handler(commands=["unsub_notif"])
def handle_help_message(message):
    if check_user_exist(user_id=message.from_user.id):
        user_subscribe(message.from_user.id)
        _send_message(
            user_id=message.from_user.id,
            message_text="Congratulations, you have successfully subscribed. Now you will receive important notifications",
        )


# MAIN COMMANDS
@bot.message_handler(commands=["help"])
def handle_help_message(message):
    if check_user_exist(user_id=message.from_user.id):
        markup = types.InlineKeyboardMarkup()

        buttons = [
            ("Cluster Status", "cluster_status"),
            ("Useful urls", "useful_urls"),
            ("Notifications", "notifications"),
            ("Domains", "domains"),
            ("Projects", "projects"),
        ]
        button_pairs = [
            (buttons[i], buttons[i + 1]) for i in range(0, len(buttons) - 1, 2)
        ]
        if len(buttons) % 2 != 0:
            button_pairs.append((buttons[-1],))
        for pair in button_pairs:
            markup.row(
                *[
                    types.InlineKeyboardButton(text=text, callback_data=callback_data)
                    for text, callback_data in pair
                ]
            )
        _send_message(
            user_id=message.from_user.id,
            message_text=f"Hello {message.from_user.first_name}, I provide a list of my capabilities",
            reply_markup=markup,
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    callback_actions = {
        "cluster_status": call_cluster_status,
        "useful_urls": call_useful_urls,
        "notifications": call_notifications,
        "domains": call_domains,
        "projects": call_projects,
    }
    action = callback_actions.get(call.data)
    if action:
        action(call.message.chat.id)


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


@bot.message_handler(commands=["about"])
def handle_about_message(message):
    if check_user_exist(user_id=message.from_user.id):
        markup_inline = types.InlineKeyboardMarkup()
        card_button = types.InlineKeyboardButton("Business Card", url=get_bcard_url())
        markup_inline.add(card_button)
        _send_message(
            user_id=message.from_user.id,
            message_text=f"""Good day, dear {message.from_user.first_name}
It is my humble pleasure to inform you that this bot has been graciously crafted by Mr. Dmitry Chistyakov. Should you wish to learn more about his endeavors and expertise, I kindly invite you to view his business card at the following link.
Thank you for your kind attention""",
            reply_markup=markup_inline,
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


def init_bot_service():
    logging.info("Init main service bot")
