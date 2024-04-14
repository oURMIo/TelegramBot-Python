import configparser
from pathlib import Path

class ConfigService:
    def __init__(self, file_path='config/config.ini'):
        realpath = Path(file_path).resolve()
        self.file_path = realpath
        try:
            self.config = configparser.ConfigParser()
            self.config.read(realpath)
        except FileNotFoundError:
            print(f"Config file not found: {realpath}")
            self.config = None

    def get_token(self):
        return str(self.config.get('TOKEN', 'BOT_TOKEN', fallback=None)) if self.config else None

    def get_admin_id(self):
        return self.config.get('ADMIN_ID', 'MAIN_ADMIN_ID', fallback=None) if self.config else None

    def get_url_dachserv(self):
        return self.config.get('SERVER_URLS', 'URL_DACHSERV', fallback=None) if self.config else None

    def get_url_chserv(self):
        return self.config.get('SERVER_URLS', 'URL_CHSERV', fallback=None) if self.config else None

    def get_check_dachserv_url(self):
        return self.config.get('CHECK_URLS', 'CHECK_DACHSERV_URL', fallback=None) if self.config else None
    
    def get_check_chserv_url(self):
        return self.config.get('CHECK_URLS', 'CHECK_CHSERV_URL', fallback=None) if self.config else None

    def get_url_project_morse(self):
        return self.config.get('PROJECT_URLS', 'URL_PROJECT_MORSE', fallback=None) if self.config else None

    def get_url_tool_domain(self):
        return self.config.get('TOOLS_URLS', 'URL_TOOL_DOMAIN', fallback=None) if self.config else None

    def get_url_tool_drive(self):
        return str(self.config.get('TOOLS_URLS', 'URL_TOOL_DRIVE', fallback=None)) if self.config else None
    
    def get_url_tool_monit(self):
        return str(self.config.get('TOOLS_URLS', 'URL_TOOL_MONIT', fallback=None)) if self.config else None
    
    def get_url_tool_nextcloud(self):
        return str(self.config.get('TOOLS_URLS', 'URL_TOOL_NEXTCLOUD', fallback=None)) if self.config else None
