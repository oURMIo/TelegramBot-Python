import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cache.cache_user import crete_user, get_users, check_exist_user, subscribe_user, unsubscribe_user, clean_cache_user, get_user


class TestCacheUser(unittest.TestCase):
    def setUp(self):
        clean_cache_user()

    def tearDown(self):
        clean_cache_user()

    def test_create_user(self):
        crete_user(user_id=1234, username="anton", first_name="Anton", last_name="Notna")
        crete_user(user_id=1235, username="loki", first_name="Loki", last_name="Ikol")
        users = get_users()
        user_first = users.get(1234)
        user_second = users.get(1235)
        self.assertEqual(len(users), 2)
        self.assertEqual(user_first.user_id, 1234)
        self.assertEqual(user_first.username, "anton")
        self.assertEqual(user_first.first_name, "Anton")
        self.assertEqual(user_first.last_name, "Notna")
        self.assertEqual(user_first.is_subscribe, False)
        self.assertEqual(user_second.user_id, 1235)
        self.assertEqual(user_second.username, "loki")
        self.assertEqual(user_second.first_name, "Loki")
        self.assertEqual(user_second.last_name, "Ikol")
        self.assertEqual(user_second.is_subscribe, False)

    def test_check_exist_user(self):
        crete_user(user_id=1234, username="anton", first_name="Anton", last_name="Notna")
        self.assertTrue(check_exist_user(1234))
        self.assertFalse(check_exist_user(9999))

    def test_subscribe_unsubscribe_user(self):
        user_id = 1234
        crete_user(user_id=user_id, username="anton", first_name="Anton", last_name="Notna")
        user = get_user(user_id)
        self.assertFalse(user.is_subscribe)

        subscribe_user(user_id)
        self.assertTrue(user.is_subscribe)

        unsubscribe_user(user_id)
        self.assertFalse(user.is_subscribe)


if __name__ == '__main__':
    unittest.main()
