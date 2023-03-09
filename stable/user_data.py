import os

from user import User, USER_DATA_DIRECTORY
from db.repositories.openai_usage import OpenAIUsageRepository



def get_users_data_total(ngt_tokens: int = 25_000):
    # initialize a variable to store the total tokens
    total_users = 0
    total_tokens = 0
    total_users_daily = 0

    # loop through all subdirectories in the parent directory
    for user_dir in os.listdir(USER_DATA_DIRECTORY):
        user = User(int(user_dir))
       
        if user.balance.amount > ngt_tokens:
            continue

        total_users += 1
        total_tokens += int(user.balance.amount)

        if not user.daily_tokens.available():
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
    rows = repository._get_all()
    
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