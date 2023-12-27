import random
import sys
sys.path.append('./src')

from file_service import FileService

file_service=FileService()

username="TestUesr"
userId=random.randint(1, 9999)

print(f"Empty users: {file_service.get_users()}")

file_service.save_user(userId, username)
print(f"Add user: {file_service.get_users()}")

file_service.save_user(userId, username)
print(f"Add again users: {file_service.get_users()}")

file_service.subscribe(userId)
print(f"Subscribe users: {file_service.get_users()}")
print(f"Subscribe list users: {file_service.get_subscribe_users()}")

file_service.unsubscribe(userId)
print(f"Unsubscribe users: {file_service.get_users()}")
print(f"Unsubscribe list users: {file_service.get_subscribe_users()}")

file_service.remove_user(userId)
print(f"Remove users: {file_service.get_users()}")
