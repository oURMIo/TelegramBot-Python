from requests_html import HTMLSession
from config.link_config import get_cluster_1_check_url, get_cluster_2_check_url


def check_cluster_status(url: str) -> bool:
    try:
        response = HTMLSession().get(url)
        result = str(response.content)
        if "working" in result or "running" in result:
            return True
        else:
            return False
    except Exception as e:
        return False


def check_cluster_1_status() -> bool:
    return check_cluster_status(get_cluster_1_check_url())


def check_cluster_2_status() -> bool:
    return check_cluster_status(get_cluster_2_check_url())
