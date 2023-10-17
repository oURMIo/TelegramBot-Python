class UserStore:
    def __init__(self):
        self.users = []

    def add_user(self, user_id):
        if isinstance(user_id, int):
            self.users.append(user_id)
        else:
            print("Invalid user_id type. Only integers are allowed.")

    def get_all_users(self):
        return self.users

    def remove_user(self, user_id):
        if user_id in self.users:
            self.users.remove(user_id)
        else:
            print(f"User with ID {user_id} not found in the user list.")
