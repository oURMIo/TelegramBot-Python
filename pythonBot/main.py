import telebot
import conf
import time
from requests_html import HTMLSession
from threading import Thread
from time import sleep

# CONFIG
bot = telebot.TeleBot(conf.TOKEN)

# Project urls
urlProjectCheck = conf.URL_PROJECT_CHECK
urlProjectMorse = conf.URL_PROJECT_MORSE

# Tool urls
urlToolDomain = conf.URL_TOOL_DOMAIN
urlToolDrive = conf.URL_TOOL_DRIVE

work = True


def sendMessageShutDown():
    file = open("INFA.txt")
    for line in file:
        id = line.partition(" ")[0]
        text = (
            "Dachserv just shut down! Check it out by following the link -"
            + urlProjectCheck,
        )
        bot.send_message(int(id), text)
    file.close()


def checkServ():
    global work
    session = HTMLSession()
    while work == True:
        try:
            response = session.get(urlProjectCheck)
            result = str(response.content)
            res = result.find("working")
            if res < 0:
                work = False
                sendMessageShutDown()
            sleep(60)
        except:
            work = False
            sendMessageShutDown()


thCheckServ = Thread(target=checkServ)
thCheckServ.start()


@bot.message_handler(commands=["start"])
def filesave(message):
    text = "Hello (〃￣︶￣)人(￣︶￣〃)! My name is Sagiri, and I am a system administrator bot capable of checking the status of servers and notifying you about their condition"
    bot.reply_to(message, text)
    file = open("INFA.txt", "a+")
    file.write(str(message.from_user.id) + " || " + str(time.ctime()) + "\n")
    file.close()


@bot.message_handler(commands=["help"])
def helping(message):
    text = """You can use these commands :
    /instruments      - List of url instruments
    /projects         - List of projects
    /for_family       - List urls for chistyakovs
    /check_dachserv   - Check server 'dachserv' status
    /check_enable     - This command should be used if you want to monitor the status of servers"""
    bot.reply_to(message, str(text))


@bot.message_handler(commands=["check_dachserv"])
def filesave(message):
    try:
        response = HTMLSession().get(urlProjectCheck)
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
    text = "List of projects : \n\n" + "• " + urlProjectMorse + "\n"
    bot.reply_to(message, text)


@bot.message_handler(commands=["instruments"])
def changeworkstatus(message):
    text = (
        "List of tools : \n\n"
        + "• domains - "
        + urlToolDomain
        + "\n"
        + "• drive   - "
        + urlToolDrive
        + "\n"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["for_family"])
def changeworkstatus(message):
    text = "List for family : \n\n" + "• drive - " + urlToolDrive + "\n"
    bot.reply_to(message, text)


# REPID
@bot.message_handler(content_types=["text"])
def repid(message):
    text = "I do not understand you. Select a function from the given list /help"
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

