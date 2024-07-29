from config.config_bot import _send_message


def call_cluster_status(chat_id: int):
    _send_message(user_id=chat_id, message_text="call_cluster_status")


def call_useful_urls(chat_id: int):
    _send_message(user_id=chat_id, message_text="call_useful_urls")


def call_notifications(chat_id: int):
    _send_message(user_id=chat_id, message_text="call_notifications")


def call_domains(chat_id: int):
    _send_message(user_id=chat_id, message_text="call_domains")


def call_projects(chat_id: int):
    _send_message(user_id=chat_id, message_text="call_projects")
