import sys
import pytest
from unittest.mock import Mock

sys.path.append("./src")

from config_service import ConfigService


def test_config_service():
    config_service = Mock(ConfigService)

    config_service.get_token.return_value = "test_token"
    config_service.get_admin_id.return_value = "test_admin_id"
    config_service.get_url_dachserv.return_value = "http://dachserv.test"
    config_service.get_url_chserv.return_value = "http://chserv.test"
    config_service.get_check_dachserv_url.return_value = "http://checkdachserv.test"
    config_service.get_check_chserv_url.return_value = "http://checkchserv.test"
    config_service.get_url_project_morse.return_value = "http://projectmorse.test"
    config_service.get_url_tool_domain.return_value = "http://tooldomain.test"
    config_service.get_url_tool_drive.return_value = "http://tooldrive.test"

    assert config_service.get_token() == "test_token"
    assert config_service.get_admin_id() == "test_admin_id"
    assert config_service.get_url_dachserv() == "http://dachserv.test"
    assert config_service.get_url_chserv() == "http://chserv.test"
    assert config_service.get_check_dachserv_url() == "http://checkdachserv.test"
    assert config_service.get_check_chserv_url() == "http://checkchserv.test"
    assert config_service.get_url_project_morse() == "http://projectmorse.test"
    assert config_service.get_url_tool_domain() == "http://tooldomain.test"
    assert config_service.get_url_tool_drive() == "http://tooldrive.test"


if __name__ == "__main__":
    pytest.main()
