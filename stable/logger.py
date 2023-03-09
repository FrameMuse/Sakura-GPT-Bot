import time
from user import User
from messages_history import MessageHistory

def log_text(text, user: User, role: MessageHistory.Role):
    with open("logs/text_log.txt", "a") as file:
        if role == MessageHistory.Role.USER:
            cost = str(int(len(text) / 0.75))
            timestamp = time.time()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            log_line = "[TEXT LOG] <" + timestamp + "> #User " + "(User_name:" + user.username + "; User_id:" + str(user.id) + ") Tokens_cost:" + cost + " >> " + text.replace("\n", " ") + "\n"
            file.write(log_line)
        if role == MessageHistory.Role.ASSISTANT:
            timestamp = time.time()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            log_line = "[TEXT LOG] <" + timestamp + "> #Bot  " + "(User_name:" + user.username + "; User_id:" + str(user.id) + ") >> " + text.replace("\n", " ") + "\n\n"
            file.write(log_line)


def log_purchase(user: User, quantity: int):
    timestamp = time.time()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    log_line = "[PURCHASE LOG] <" + timestamp + ">" + "(User_name:" + user.username + "; User_id:" + str(user.id) + ") >> " + str(quantity) + " Tokens\n"
    with open("logs/purchase_log.txt", "a") as file:
        file.write(log_line)
