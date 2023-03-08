from chat_user import ChatUser
from time import time

# TODO: add consts

def get_daily(user_id:int):

    chat_user = ChatUser("",user_id)
    chat_user.restore_settings()

    daily_tokens = 100

    if time() - chat_user.last_daily > 3600*24:
        chat_user.tokens+=daily_tokens
        chat_user.last_daily = time()
        chat_user.save()
    else:
        return None
    
    return daily_tokens