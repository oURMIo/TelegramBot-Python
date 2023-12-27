import os
import json
from datetime import datetime

class FileService:
    def __init__(self, filename='files/user_data.json'):
        self.filename = filename
        self.user_data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as json_file:
                return json.load(json_file)
        else:
            return {'users': []}

    def save_user(self, user_id, username):
        existing_user = next((user for user in self.user_data['users'] if user['userId'] == user_id), None)
        if not existing_user:
            time_registered = str(datetime.now())
            user_info = {'userId': user_id, 'username': username, 'subscribe': False, 'time_registered': time_registered}
            self.user_data['users'].append(user_info)
            self._save_data()

    def remove_user(self, user_id):
        for user in self.user_data['users']:
            if user['userId'] == user_id:
                self.user_data['users'].remove(user)
                self._save_data()

    def get_users(self):
        return self.user_data['users']

    def _save_data(self):
        with open(self.filename, 'w') as json_file:
            json.dump(self.user_data, json_file)

    def subscribe(self, user_id):
        for user in self.user_data['users']:
            if user['userId'] == user_id:
                user['subscribe'] = True
                self._save_data()
                break

    def unsubscribe(self, user_id):
        for user in self.user_data['users']:
            if user['userId'] == user_id:
                user['subscribe'] = False
                self._save_data()
                break

    def get_subscribe_users(self):
        subscribe_users = [user['userId'] for user in self.user_data['users'] if user['subscribe']]
        return subscribe_users
    
    def check_user_exists(self, user_id):
        return any(user['userId'] == user_id for user in self.user_data['users'])
