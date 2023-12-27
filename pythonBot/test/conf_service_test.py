import sys
sys.path.append('./src')

from config_service import ConfigService

config_service = ConfigService()
print(f"Token ID: {config_service.get_token()}")
print(f"Admin ID: {config_service.get_admin_id()}")
print(f"url : {config_service.get_url_dachserv()}")
print(f"url : {config_service.get_url_chserv()}")
print(f"url : {config_service.get_check_dachserv_url()}")
print(f"url : {config_service.get_check_chserv_url()}")
print(f"url : {config_service.get_url_project_morse()}")
print(f"url : {config_service.get_url_tool_domain()}")
print(f"url : {config_service.get_url_tool_drive()}")
