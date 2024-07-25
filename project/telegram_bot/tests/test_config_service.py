import unittest
from unittest.mock import patch, mock_open
from service.config_service import load_config, get_bot_token, get_main_admin_id


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
            load_config("dummy_path")

        self.assertEqual(get_bot_token(), "test_token")
        self.assertEqual(get_main_admin_id(), 123)

    @patch("service.config_service.Path.is_file", return_value=False)
    def test_load_config_file_not_found(self, mock_is_file):
        load_config("dummy_path")
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
            load_config("dummy_path")

        self.assertEqual(get_bot_token(), "test_token")
        self.assertEqual(get_main_admin_id(), 0)


if __name__ == "__main__":
    unittest.main()
