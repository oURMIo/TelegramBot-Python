import time
import logging
import time
from datetime import datetime
from threading import Thread
from config.log_config import setup_logging
from config.bot_config import _send_message
from config.link_config import get_webcm_bot_tool_url
from service.user_service import user_get_subscribe_all
from service.callback_service import fetch_json
from model.wcm_bot_tool import parse_wcmbot_tool_json
from utils.cluster_util import check_cluster_1_status, check_cluster_2_status

# Setup logging
setup_logging()

is_work_cluster1: bool = check_cluster_1_status()
counter_status_cluster1 = 0

is_work_cluster2: bool = check_cluster_2_status()
counter_status_cluster2 = 0


def check_status(cluster_name, check_function, is_work, counter, shutdown_message):
    while True:
        flag = check_function()
        if flag is False and is_work:
            counter += 1
            if counter == 2:
                subscribe_ids = user_get_subscribe_all()
                logging.info(
                    "Send '%s shutdown' message to all subscribed users: %s",
                    cluster_name,
                    subscribe_ids,
                )
                is_work = False
                for chat_id in subscribe_ids:
                    _send_message(user_id=chat_id, message_text=shutdown_message)
        else:
            counter = 0
        time.sleep(60)


def demon_check_status_cluster1():
    global is_work_cluster1, counter_status_cluster1
    shutdown_message = (
        "The <b>Dach</b> cluster has status:<code>'SHUTDOWN'</code>. "
        "Please check the cluster's status or contact my creator"
    )
    check_status(
        "dach",
        check_cluster_1_status,
        is_work_cluster1,
        counter_status_cluster1,
        shutdown_message,
    )


def demon_check_status_cluster2():
    global is_work_cluster2, counter_status_cluster2
    shutdown_message = (
        "The <b>Chist</b> cluster has status:<code>'SHUTDOWN'</code>. "
        "Please check the cluster's status or contact my creator"
    )
    check_status(
        "chist",
        check_cluster_2_status,
        is_work_cluster2,
        counter_status_cluster2,
        shutdown_message,
    )


def demon_domain_notification():
    sent_flag = True
    while True:
        data = fetch_json(get_webcm_bot_tool_url())
        parsed_data = parse_wcmbot_tool_json(data)
        start_date = datetime.fromisoformat(parsed_data[0].last_notif_data)
        current_date = datetime.now()
        days_passed = (current_date - start_date).days
        days_left = 23 - days_passed % 24
        if days_left == 0 and sent_flag:
            subscribe_ids = user_get_subscribe_all()
            ms_text = (
                "Good day! It's time to freshen up the domain names for our servers."
            )
            for chat_id in subscribe_ids:
                _send_message(user_id=chat_id, message_text=ms_text)
            sent_flag = False
            time.sleep(86400)
        time.sleep(43200)
        sent_flag = True


def init_demons():
    try:
        thread_status_cluster1 = Thread(target=demon_check_status_cluster1)
        thread_status_cluster1.start()
        thread_status_cluster2 = Thread(target=demon_check_status_cluster2)
        thread_status_cluster2.start()
        thread_domain_notification = Thread(target=demon_domain_notification)
        thread_domain_notification.start()
    except Exception as e:
        logging.exception("Got exception in service daemon, e:%r", e)
