import time
from chat_user import ChatUser

def log_text(text, user: ChatUser , role= "Bot"):
    with open("logs/text_log.txt", "a") as file:
        if role == "User":
            cost = str(int(len(text) / 0.75))
            timestamp = time.time()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            log_line = "[TEXT LOG] <" + timestamp + "> #User " + "(User_name:" + user.user_name + "; User_id:" + str(user.user_id) + ") Tokens_cost:" + cost + " >> " + text.replace("\n", " ") + "\n"
            file.write(log_line)
        else:
            timestamp = time.time()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            log_line = "[TEXT LOG] <" + timestamp + "> #Bot  " + "(User_name:" + user.user_name + "; User_id:" + str(user.user_id) + ") >> " + text.replace("\n", " ") + "\n\n"
            file.write(log_line)


def log_purchase(user: ChatUser , quantity , role= "Bot"):
    timestamp = time.time()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    log_line = "[PURCHASE LOG] <" + timestamp + ">" + "(User_name:" + user.user_name + "; User_id:" + str(user.user_id) + ") >> " + str(quantity) + " Tokens\n"
    with open("logs/purchase_log.txt", "a") as file:
        file.write(log_line)
