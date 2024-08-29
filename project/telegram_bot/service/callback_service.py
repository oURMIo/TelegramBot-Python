from telebot import types
from requests_html import HTMLSession
import logging
from datetime import datetime
from config.log_config import setup_logging
from config.bot_config import _send_message
from config.link_config import (
    get_webcm_tool_url,
    get_webcm_project_url,
    get_webcm_bot_tool_url,
)
from model.link_info import parse_linkinfo_json
from model.wcm_bot_tool import parse_wcmbot_tool_json

# Setup logging
setup_logging()


def call_cluster_status(chat_id: int):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_check_dachserv = types.KeyboardButton("/check_cluster_dach")
    btn_check_chserv = types.KeyboardButton("/check_cluster_chserv")
    markup.add(btn_check_dachserv, btn_check_chserv)
    _send_message(user_id=chat_id, message_text="Select cluster", reply_markup=markup)


def call_useful_urls(chat_id: int):
    data = fetch_json(get_webcm_tool_url())
    parsed_data = parse_linkinfo_json(data)
    markup = types.InlineKeyboardMarkup()
    for item in parsed_data:
        card_button = types.InlineKeyboardButton(str(item.name), url=item.link)
        markup.add(card_button)
    _send_message(user_id=chat_id, message_text="Useful URLs:", reply_markup=markup)


def call_notifications(chat_id: int):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_sub = types.KeyboardButton("/sub_notif")
    btn_unsub = types.KeyboardButton("/unsub_notif")
    markup.add(btn_sub, btn_unsub)
    _send_message(
        user_id=chat_id,
        message_text="Select whether you need server status notifications and other useful information",
        reply_markup=markup,
    )


def call_domains(chat_id: int):
    data = fetch_json(get_webcm_bot_tool_url())
    parsed_data = parse_wcmbot_tool_json(data)
    if not parsed_data:
        exit()

    start_date = datetime.fromisoformat(parsed_data[0].last_notif_data)
    current_date = datetime.now()
    days_passed = (current_date - start_date).days
    days_left = 23 - days_passed % 24
    if days_left != 0:
        _send_message(
            user_id=chat_id,
            message_text=f"My Lord, may I gently remind you that there are only <b>{days_left}</b> days left until the renewal of the domain name",
        )
    else:
        _send_message(
            user_id=chat_id,
            message_text=f"My Lord, I humbly remind you that today is the day to renew the domain name",
        )


def call_projects(chat_id: int):
    data = fetch_json(get_webcm_project_url())
    parsed_data = parse_linkinfo_json(data)
    ms_text = """Projects:\n"""
    for item in parsed_data:
        ms_text += f"""• {item.name} - link:[{item.link}]\n"""
    _send_message(user_id=chat_id, message_text=ms_text)


def fetch_json(url: str):
    try:
        response = HTMLSession().get(url)
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return []
