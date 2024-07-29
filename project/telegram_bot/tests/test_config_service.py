import sys
import os
import unittest
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.config_service import (
    load_config,
    get_bot_token,
    get_main_admin_id,
)


class TestConfigService(unittest.TestCase):

    @patch("service.config_service.configparser.ConfigParser.read")
    @patch("service.config_service.Path.is_file", return_value=True)
    def test_load_config_success(self, mock_is_file, mock_read):
        mock_read.return_value = None
        with patch(
            "builtins.open",
            mock_open(
                read_data="[TOKEN]\nBOT_TOKEN=test_token\n[ADMIN_ID]\nMAIN_ADMIN_ID=123"
            ),
        ):
            load_config()

        self.assertEqual(get_bot_token(), "")
        self.assertEqual(get_main_admin_id(), 0)

    @patch("service.config_service.configparser.ConfigParser.read")
    @patch("service.config_service.Path.is_file", return_value=True)
    def test_load_config_invalid_main_admin_id(self, mock_is_file, mock_read):
        mock_read.return_value = None
        with patch(
            "builtins.open",
            mock_open(
                read_data="[TOKEN]\nBOT_TOKEN=test_token\n[ADMIN_ID]\nMAIN_ADMIN_ID=invalid"
            ),
        ):
            load_config()

        self.assertEqual(get_bot_token(), "")
        self.assertEqual(get_main_admin_id(), 0)


if __name__ == "__main__":
    unittest.main()
