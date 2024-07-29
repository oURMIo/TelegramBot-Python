from requests_html import HTMLSession


def check_server_status(url):
    try:
        response = HTMLSession().get(url)
        result = str(response.content)
        if "working" in result or "running" in result:
            return True
        else:
            return False
    except Exception as e:
        return False
