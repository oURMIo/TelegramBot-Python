import sys
import os
import unittest
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.config_service import load_config, get_bot_token, get_main_admin_id


class TestConfigService(unittest.TestCase):
    CONFIG_DATA_VALID = "[TOKEN]\nBOT_TOKEN=test_token\n[ADMIN_ID]\nMAIN_ADMIN_ID=123"
    CONFIG_DATA_INVALID = (
        "[TOKEN]\nBOT_TOKEN=test_token\n[ADMIN_ID]\nMAIN_ADMIN_ID=invalid"
    )
    CONFIG_DATA_NO_TOKEN = "[ADMIN_ID]\nMAIN_ADMIN_ID=123"
    CONFIG_DATA_NO_ADMIN_ID = "[TOKEN]\nBOT_TOKEN=test_token"

    @patch("service.config_service.configparser.ConfigParser.read", return_value=None)
    @patch("service.config_service.Path.is_file", return_value=True)
    def test_load_config(self, mock_is_file, mock_read):
        for data, expected_id in [
            (self.CONFIG_DATA_VALID, 0),
            (self.CONFIG_DATA_INVALID, 0),
            (self.CONFIG_DATA_NO_TOKEN, 0),
            (self.CONFIG_DATA_NO_ADMIN_ID, 0),
        ]:
            with patch("builtins.open", mock_open(read_data=data)):
                load_config()
                self.assertEqual(get_bot_token(), "")
                self.assertEqual(get_main_admin_id(), expected_id)

    @patch("service.config_service.configparser.ConfigParser.read", return_value=None)
    @patch("service.config_service.Path.is_file", return_value=False)
    def test_load_config_file_not_found(self, mock_is_file, mock_read):
        load_config()
        self.assertEqual(get_bot_token(), "")
        self.assertEqual(get_main_admin_id(), 0)

    @patch("service.config_service.configparser.ConfigParser.read", return_value=None)
    @patch("service.config_service.Path.is_file", return_value=True)
    def test_load_config_empty_file(self, mock_is_file, mock_read):
        with patch("builtins.open", mock_open(read_data="")):
            load_config()
            self.assertEqual(get_bot_token(), "")
            self.assertEqual(get_main_admin_id(), 0)


if __name__ == "__main__":
    unittest.main()
