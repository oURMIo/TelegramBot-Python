import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from service.service_user import (
    _UserFileService,
    user_save,
    user_subscribe,
    user_unsubscribe,
    user_get_all,
    user_check_exist,
)


class TestUserFileService(unittest.TestCase):

    def setUp(self):
        _UserFileService._instance = None
        self.service = _UserFileService(
            filename="./telegram_bot/data/test_user_data.json"
        )

    def tearDown(self):
        _UserFileService._instance = None

    @patch("builtins.open", new_callable=mock_open, read_data='{"users": []}')
    def test_load_data_non_existent_file(self, mock_file):
        with patch("os.path.exists", return_value=False):
            service = _UserFileService(
                filename="./telegram_bot/data/test_user_data.json"
            )
            self.assertEqual(service.get_users(), [])
            mock_file.assert_not_called()

    @patch("builtins.open", new_callable=mock_open)
    def test_unsubscribe_user(self, mock_file):
        user_save(8, "testuser4")
        user_subscribe(8)
        user_unsubscribe(8)
        self.assertFalse(user_get_all()[0]["subscribe"])

    @patch("builtins.open", new_callable=mock_open)
    def test_check_user_exists(self, mock_file):
        user_save(9, "testuser5")
        self.assertTrue(user_check_exist(9))
        self.assertFalse(user_check_exist(10))

    @patch("builtins.open", new_callable=mock_open)
    def test_save_data(self, mock_file):
        service = _UserFileService(filename="./telegram_bot/data/test_user_data.json")
        service.save_user(5, "testuser5")
        mock_file().write.assert_called()


if __name__ == "__main__":
    unittest.main()
