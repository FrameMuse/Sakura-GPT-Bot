import os
import json
from pathlib import Path

from daily import get_daily
from db.repositories.openai_usage import OpenAIUsageRepository

# specify the parent directory that contains the folders with settings.json files
parent_dir = "user-data"

def get_users_data_total(ngt_tokens: int = 25_000):
    # initialize a variable to store the total tokens
    total_users = 0
    total_tokens = 0
    total_users_daily = 0

    # loop through all subdirectories in the parent directory
    for user_dir in os.listdir(parent_dir):
        # check if the subdirectory contains a settings.json file
        settings_file = Path(parent_dir + "/" + user_dir + "/settings.json")
        if not settings_file.is_file():
            continue

        settings_content = settings_file.read_text("utf-8")
        settings_content_json: dict = json.loads(settings_content)

        if "tokens" not in settings_content_json:
            continue

        # print(settings_content_json)

        daily_tokens = get_daily(int(user_dir))
        settings_tokens = settings_content_json["tokens"]
        if settings_tokens > ngt_tokens:
            continue

        total_users += 1
        total_tokens += int(settings_tokens)

        if not daily_tokens:
            total_users_daily += 1


    return total_tokens, total_users, total_users_daily
    # return total_tokens

print("--- [Not greater than 25_000 tokens] ---")
users_total = get_users_data_total(25_000)
print(f"Total tokens {users_total[0]} and users: {users_total[1]}")
print(f"Tokens per user: {users_total[0] / users_total[1]}")
print(f"Users that already got daily tokens: {users_total[2]}")

print("\n")

print("--- [Not greater than 500 tokens] ---")
users_total = get_users_data_total(500)
print(f"Total tokens {users_total[0]} and users: {users_total[1]}")
print(f"Tokens per user: {users_total[0] / users_total[1]}")
print(f"Users that already got daily tokens: {users_total[2]}")

print("\n")

print("--- [Not greater than 100 tokens] ---")
users_total = get_users_data_total(100)
print(f"Total tokens {users_total[0]} and users: {users_total[1]}")
print(f"Tokens per user: {users_total[0] / users_total[1]}")
print(f"Users that already got daily tokens: {users_total[2]}")

print("\n")

print("--- [Not greater than 40 tokens] ---")
users_total = get_users_data_total(40)
print(f"Total tokens {users_total[0]} and users: {users_total[1]}")
print(f"Tokens per user: {users_total[0] / users_total[1]}")
print(f"Users that already got daily tokens: {users_total[2]}")


def get_requests():
    repository = OpenAIUsageRepository()
    rows = repository.get_all()
    
    texts = 0
    images = 0

    for row in rows:
        if row.type == repository.Type.TEXT.name:
            texts += 1
        if row.type == repository.Type.IMAGE.name:
            images += 1

    return texts, images

print("\n")

requests = get_requests()
print(f"Total text requests: {requests[0]} and image requests: {requests[1]}")
print(f"Image per text: {requests[1] / requests[0]}")