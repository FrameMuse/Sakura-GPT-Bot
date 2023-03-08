from db.repositories.promocodes import PromocodesRepository
from chat_user import ChatUser


def activate_promocode(code:str,user_id:int):
    chat_user = ChatUser("",user_id)
    chat_user.restore_settings()

    repository = PromocodesRepository()
    promocode = repository.find(code)
    repository.close()

    if promocode == None:
        return None
    
    chat_user.tokens += promocode[2]
    chat_user.activated_promocodes.append(code)
    chat_user.save()

    return promocode[2]
 