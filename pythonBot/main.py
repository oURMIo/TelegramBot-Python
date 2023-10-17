import telebot
import conf
import user
import time
import logging
from requests_html import HTMLSession
from threading import Thread
from time import sleep

# CONFIG
bot = telebot.TeleBot(conf.TOKEN)

# ADMIN ID

admin_id = int(conf.ADMIN_ID)

# PROJECT URLS
url_project_check = conf.URL_PROJECT_CHECK
url_project_morse = conf.URL_PROJECT_MORSE

# TOOL URLS
url_tool_domain = conf.URL_TOOL_DOMAIN
url_tool_drive = conf.URL_TOOL_DRIVE

# LOGGING
logger = logging.getLogger('Logger')
logger.setLevel(logging.DEBUG)
file_handler1 = logging.FileHandler('concole.log', mode='w')
file_handler1.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] - [%(message)s]')
file_handler1.setFormatter(formatter)
logger.addHandler(file_handler1)
# %s for string, %d for number

# GLOBAL VARIBLES
user_store = user.UserStore()
work = True
TIME_OUT = 30
SHUTDOWN_MESSAGE = "Dachserv just shut down! Check it out by following the link -"


def send_shutdown_message():
    user_ids = user_store.get_all_users()
    message = SHUTDOWN_MESSAGE + url_project_check
    for user_id in user_ids:
        bot.send_message(int(user_id), message)


def check_server():
    global work
    session = HTMLSession()
    while work:
        try:
            response = session.get(url_project_check)
            if "working" not in response.text:
                work = False
                send_shutdown_message()
            sleep(TIME_OUT)
        except Exception as e:
            work = False
            send_shutdown_message()


def check_periodically():
    global work
    session = HTMLSession()
    
    while not work:
        try:
            response = session.get(url_project_check)
            if "working" in response.text:
                work = True
            sleep(20 * 60)
        except Exception as e:
            sleep(20 * 60)


@bot.message_handler(commands=["start"])
def filesave(message):
    text = "Hello (〃￣︶￣)人(￣︶￣〃)! My name is Sagiri, and I am a system administrator bot capable of checking the status of servers and notifying you about their condition"
    bot.reply_to(message, text)
    logger.info("Got new user with id-'%d'", message.from_user.id)


@bot.message_handler(commands=["help"])
def helping(message):
    text = """You can use these commands :
    /instruments      - List of url instruments
    /projects         - List of projects
    /for_family       - List urls for chistyakovs
    /subscribe        - Subscription to notifications
    /unsubscribe      - Unsubscribe from notifications
    /check_dachserv   - Check server 'dachserv' status
    /check_enable     - This command should be used if you want to monitor the status of servers"""
    bot.reply_to(message, str(text))


@bot.message_handler(commands=["subscribe"])
def filesave(message):
    text = "You have subscribed successfully. Congratulations! \n" + "You will now receive notifications. If you do not want to receive notifications, use the command /unsubscribe"
    bot.reply_to(message, text)
    user_store.add_user(int(message.from_user.id))
    logger.debug("User with id:'%d' had subscribed", message.from_user.id)


@bot.message_handler(commands=["unsubscribe"])
def filesave(message):
    text = "You unsubscribed from the notification"
    bot.reply_to(message, text)
    user_store.remove_user(int(message.from_user.id))
    logger.debug("User with id:'%d' had unsubscribed", message.from_user.id)


@bot.message_handler(commands=["subscribe_list"])
def filesave(message):
    if message.from_user.id == admin_id:
        user_mas = user_store.get_all_users()
        text = ", ".join(map(str, user_mas))
        bot.reply_to(message, text)
    else:
        text = "Permission denied"
        bot.reply_to(message, text)


@bot.message_handler(commands=["check_dachserv"])
def filesave(message):
    try:
        response = HTMLSession().get(url_project_check)
        result = str(response.content)
        res = result.find("working")
        if res > 0:
            bot.reply_to(message, "Now, dach-server is working")
        else:
            bot.reply_to(message, "dach-server down. You should check its status")
    except:
        bot.reply_to(message, "dach-server down. You should check its status")


@bot.message_handler(commands=["check_enable"])
def changeworkstatus(message):
    global work
    work = True
    bot.reply_to(message, "Now the check is working again ")


@bot.message_handler(commands=["projects"])
def changeworkstatus(message):
    text = "List of projects : \n\n" + "• " + url_project_morse + "\n"
    bot.reply_to(message, text)


@bot.message_handler(commands=["instruments"])
def changeworkstatus(message):
    text = (
        "List of tools : \n\n"
        + "• domains - "
        + url_tool_domain
        + "\n"
        + "• drive   - "
        + url_tool_drive
        + "\n"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["for_family"])
def changeworkstatus(message):
    text = "List for family : \n\n" + "• drive - " + url_tool_drive + "\n"
    bot.reply_to(message, text)


# REPID
@bot.message_handler(content_types=["text"])
def repid(message):
    text = "I do not understand you. Select a function from the given list /help"
    bot.send_message(message.chat.id, text)


# THREADS
thread_check_enable = Thread(target=check_periodically)
thread_check_enable.start()
thread_check_serv = Thread(target=check_server)
thread_check_serv.start()

bot.polling(none_stop=True)
