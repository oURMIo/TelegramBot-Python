import telebot
from telebot import types
import logging
from logging.handlers import RotatingFileHandler
import os
from requests_html import HTMLSession
from threading import Thread
import time
import datetime

from config_service import ConfigService
from file_service import FileService

LOG_DIR = './logs/'
MAX_LOG_SIZE = 100 * 1024 * 1024  # 100 MB

os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, 'console.log')
with open(log_file, 'w'):
    pass

handler = RotatingFileHandler(log_file, maxBytes=MAX_LOG_SIZE, backupCount=1)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] - [%(message)s]')
handler.setFormatter(formatter)

logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.DEBUG)
# %s for string, %d for number

config_service = ConfigService()
file_service=FileService()

token = config_service.get_token()

if not token:
    logging.error("Bot token not found. Make sure to provide a valid token.")
    exit()

bot = telebot.TeleBot(token)
# message.from_user.id
# message.from_user.first_name
# message.from_user.last_name
# message.from_user.username


def check_server_status(url):
    try:
        response = HTMLSession().get(url)
        result = str(response.content)
        if "working" in result:
            return True
        else:
            logging.info("Cluster has status 'SHUTDOWN', with url:%s", url)
            return False
    except Exception as e:
        logging.info("Cluster has status 'SHUTDOWN', with url:%s", url)
        return False


flag_dach_work = check_server_status(config_service.get_check_dachserv_url())
dach_status_counter = 0

flag_chserv_work = check_server_status(config_service.get_check_chserv_url())
chserv_status_counter = 0


def demon_check_dach_status():
    while True:
        global flag_dach_work
        global dach_status_counter
        check_url = config_service.get_check_dachserv_url()
        flag = check_server_status(check_url)
        if flag is False and flag_dach_work is True:
            subscribe_ids = file_service.get_subscribe_users()
            dach_status_counter += 1
            if dach_status_counter == 2:
                logging.info("Send 'dach shutdown' message to all subscribe users:'%d'", subscribe_ids)
                flag_dach_work = False
                text = "The Dach server has status:'SHUTDOWN'. Please check the cluster's status or contact my creator."
                for chat_id in subscribe_ids:
                    bot.send_message(chat_id, text)
        else:
            dach_status_counter = 0
        time.sleep(60)


def demon_check_chserv_status():
    while True:
        global flag_chserv_work
        global chserv_status_counter
        check_url = config_service.get_check_chserv_url()
        flag = check_server_status(check_url)
        if flag is False and flag_chserv_work is True:
            subscribe_ids = file_service.get_subscribe_users()
            chserv_status_counter += 1
            if chserv_status_counter == 2:
                logging.info("Send 'chserv shutdown' message to all subscribe users:'%d'", subscribe_ids)
                flag_chserv_work = False
                text = "The Chist server has status:'SHUTDOWN'. Please check the cluster's status or contact my creator."
                for chat_id in subscribe_ids:
                    bot.send_message(chat_id, text)
        else:
            chserv_status_counter = 0
        time.sleep(60)


def demon_domain_notification():
    start_date = datetime.datetime(2024, 4, 30)
    while True:
        current_date = datetime.datetime.now()
        days_passed = (current_date - start_date).days
        if days_passed % 23 == 0:
            logging.info("Monthly domain update notification")
            subscribe_ids = file_service.get_subscribe_users()
            text = "Good day! It's time to freshen up the domain names for our servers. Please follow the link:"
            markup_inline = types.InlineKeyboardMarkup()
            domain_button = types.InlineKeyboardButton("domains", url=config_service.get_url_tool_domain())
            markup_inline.add(domain_button)
            for chat_id in subscribe_ids:
                bot.send_message(chat_id, text, reply_markup = markup_inline)
        current_date += datetime.timedelta(days=1)
        time.sleep(86400)


# REQYEST MESSAGES
@bot.message_handler(commands=["start"])
def start_message(message):
    name = message.from_user.first_name
    message_text = f"Hello {name}. My name is Sagiri, and I am a system administrator bot capable of checking the status of servers and notifying you about their condition"
    bot.reply_to(message, message_text)
    file_service.save_user(message.from_user.id, name)
    logging.info("Got new user %s with ID:'%d'", name, message.from_user.id)


@bot.message_handler(commands=["help"])
def start_message(message):
    if check_contains_user(message):
        username = message.from_user.first_name
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 4
        markup.add(types.InlineKeyboardButton(text="Tools", callback_data="tools"),
                   types.InlineKeyboardButton(text="Projects", callback_data="projects"),
                   types.InlineKeyboardButton(text="For family", callback_data="for_chistyakov"),
                   types.InlineKeyboardButton(text="Notifications", callback_data="notifications"))
        message_text = f"Hello {username}, I provide a list of my capabilities"
        bot.send_message(chat_id=message.from_user.id, text=message_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "tools":
        sub_tools_message(call.message.chat.id)
    elif call.data == "projects":
        sub_projects_message(call.message.chat.id)
    elif call.data == "for_chistyakov":
        sub_chistyakov_message(call.message.chat.id, call.message.chat.first_name)
    elif call.data == "notifications":
        sub_notification_message(call.message.chat.id)


@bot.message_handler(commands=["for_chistyakov"])
def chistyakov_message(message):
    sub_chistyakov_message(message.from_user.id, message.from_user.first_name)


def sub_chistyakov_message(chat_id, name):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Family's folder", url=config_service.get_url_tool_drive())
    markup.add(button1)
    bot.send_message(chat_id, "Hello "+name+", greetings to the creator. Your link:", reply_markup=markup)


@bot.message_handler(commands=["tools"])
def tools_message(message):
    sub_tools_message(message.from_user.id)


def sub_tools_message(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_check_status = types.KeyboardButton("Server status")
    btn_instrument_url = types.KeyboardButton("Helpful urls")
    btn_price_request = types.KeyboardButton("Price request")
    btn_left_domain = types.KeyboardButton("Days Left Domain")
    markup.add(btn_check_status, btn_instrument_url, btn_price_request, btn_left_domain)
    bot.send_message(chat_id, "Select an action select an action using the buttons", reply_markup=markup)
      

@bot.message_handler(commands=["projects"])
def projects_message(message):
    sub_projects_message(message.from_user.id)


def sub_projects_message(chat_id):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Morse translator", url=config_service.get_url_project_morse())
    markup.add(button1)
    bot.send_message(chat_id, "All working projects:", reply_markup=markup)


@bot.message_handler(commands=["check_dach_server"])
def check_dach_server_message(message):
    global flag_dach_work
    if check_contains_user(message):
        check_url = config_service.get_check_dachserv_url()
        status_flag = check_server_status(check_url)
        if status_flag:
            flag_dach_work = True
            message_text = "Dach server status: 'WORKING'"
        else:
            flag_dach_work = False
            message_text = "Dach server status: 'SHUTDOWN'"
        bot.send_message(message.from_user.id, message_text, reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=["check_chist_server"])
def check_chist_server_message(message):
    global flag_chserv_work
    if check_contains_user(message):
        check_url = config_service.get_check_chserv_url()
        status_flag = check_server_status(check_url)
        if status_flag:
            flag_chserv_work = True
            message_text = "Chist server status: 'WORKING'"
        else:
            flag_chserv_work = False
            message_text = "Chist server status: 'SHUTDOWN'"
        bot.send_message(message.from_user.id, message_text, reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=["notification"])
def notification_message(message):
    sub_notification_message(message.from_user.id)


def sub_notification_message(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_check_dachserv = types.KeyboardButton("/subscribe")
    btn_check_chserv = types.KeyboardButton("/unsubscribe")
    markup.add(btn_check_dachserv, btn_check_chserv)
    bot.send_message(chat_id, "Select whether you need server status notifications and other useful information", reply_markup=markup)


@bot.message_handler(commands=["subscribe"])
def subscribe_message(message):
    if check_contains_user(message):
        file_service.subscribe(message.from_user.id)
        bot.send_message(message.from_user.id, "Congratulations, you have successfully subscribed. Now you will receive important notifications",
                         reply_markup = telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=["unsubscribe"])
def unsubscribe_message(message):
    if check_contains_user(message):
        file_service.unsubscribe(message.from_user.id)
        bot.send_message(message.from_user.id, "You have unsubscribed from receiving notifications. To start receiving them again, use the command /subscribe",
                         reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(content_types=["text"])
def responsi_text_message(message):
    if check_contains_user(message):
        markup = types.ReplyKeyboardRemove()
        match message.text.lower():
            case "server status":
                sub_checking_service_status(message)
            
            case "helpful urls":
                sub_helpful_urls(message)

            case "days left domain":
                sub_days_left_domain(message)

            case "price request":
                sub_price_request(message)

            case _:
                bot.send_message(message.from_user.id, "I do not understand you. Select a function from the given list /help", reply_markup=markup)


def sub_checking_service_status(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_check_dachserv = types.KeyboardButton("/check_dach_server")
    btn_check_chserv = types.KeyboardButton("/check_chist_server")
    markup.add(btn_check_dachserv, btn_check_chserv)
    bot.send_message(message.from_user.id, "Select cluster".format(message.from_user), reply_markup=markup)


def sub_helpful_urls(message):
    markup_remove = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Helpful urls", reply_markup=markup_remove)
    markup_inline = types.InlineKeyboardMarkup()
    domain_button = types.InlineKeyboardButton("domains", url=config_service.get_url_tool_domain())
    drive_button = types.InlineKeyboardButton("drive", url=config_service.get_url_tool_drive())
    monit_button = types.InlineKeyboardButton("chserv monit", url=config_service.get_url_tool_monit())
    cloude_button = types.InlineKeyboardButton("nextcloud", url=config_service.get_url_tool_nextcloud())
    markup_inline.add(domain_button, drive_button, monit_button, cloude_button)
    bot.send_message(message.from_user.id, "Choose a tool:", reply_markup = markup_inline)


def sub_price_request(message):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "I apologize, but not supported now".format(message.from_user),reply_markup=markup)


def sub_days_left_domain(message):
    markup = telebot.types.ReplyKeyboardRemove()
    start_date = datetime.datetime(2024, 4, 30)
    current_date = datetime.datetime.now()
    days_passed = (current_date - start_date).days
    name = message.from_user.first_name
    days_left = 23 - days_passed % 23
    bot.send_message(message.from_user.id, f"Dear {name}. Just a gentle reminder, there are '{days_left}' days left until the renewal of the domain name.".format(message.from_user),reply_markup=markup)


def check_contains_user(message):
    if not file_service.check_user_exists(message.from_user.id):
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Excuse me, could you please use the '/start' command from the very beginning".format(message.from_user),reply_markup=markup)
        return False
    return True


if __name__ == '__main__':
    try:
        thread_check_dachserv = Thread(target=demon_check_dach_status)
        thread_check_dachserv.start()
        thread_check_chserv = Thread(target=demon_check_chserv_status)
        thread_check_chserv.start()
        thread_check_domain = Thread(target=demon_domain_notification)
        thread_check_domain.start()
        bot.polling(none_stop=True)
    except telebot.apihelper.ApiException as e:
        logging.exception("Telegram API Error: %r", e)
    except Exception as e:
        logging.exception("Error occurred while polling: %r", e)
