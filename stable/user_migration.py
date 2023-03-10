import json

from pathlib import Path
from user import User, USER_DATA_DIRECTORY

def get_deprected_user_settings(user_id: int):
    path = Path(f"{USER_DATA_DIRECTORY}/{str(user_id)}/settings.json")
    if not path.exists(): return

    try:
        content = json.loads(path.read_text())
        return content
    except Exception as error:
        print(error)

def migrate_user(user_id: int):
    settings = get_deprected_user_settings(user_id)
    if not settings: return

    personality = settings["personality"]
    balance = settings["tokens"]
    username = settings["user_name"]
    last_daily = settings["last_daily"]


    user = User(user_id)
    user.personality = personality
    user.balance.set_amount(float(balance))
    user.username = username
    user.daily_tokens.set_obtained(last_daily)



for user_id in User.findall_ids():
    migrate_user(int(user_id))
