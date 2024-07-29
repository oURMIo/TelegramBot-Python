from requests_html import HTMLSession
from config.config_link import get_cluster_1_check_url, get_cluster_2_check_url


def check_cluster_status(url: str):
    try:
        response = HTMLSession().get(url)
        result = str(response.content)
        if "working" in result or "running" in result:
            return True
        else:
            return False
    except Exception as e:
        return False


def check_cluster_1_status():
    global cluster_1_status
    flag = check_cluster_status(get_cluster_1_check_url())
    cluster_1_status = flag
    return flag


def check_cluster_2_status():
    global cluster_2_status
    flag = check_cluster_status(get_cluster_2_check_url())
    cluster_2_status = flag
    return flag


# Global constants
cluster_1_status = check_cluster_1_status()
cluster_2_status = check_cluster_2_status()
