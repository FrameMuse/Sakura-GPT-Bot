# def log(text, role, user_id ,filename="logs.txt"):
#     with open(filename, 'a') as file:
#         if role == "Bot":
#             file.write("<" + str(time()) + " " + role + " " + str(user_id) + "> "+text + '\n\n')
#         else:
#             file.write("<" + str(time()) + " " + role + " " + str(user_id) + "> "+text + '\n')

import time
from chat_user import ChatUser
LOGS_PATH = "logs/"


def log_text(text, user: ChatUser , role= "Bot", filename= LOGS_PATH + "logs.txt"):
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



# chat_user = ChatUser("nasme",123321)

# log_text("Ask",chat_user,"User")
# log_text("hehe fdsfds fdsfds\n fdsfds\nfdsfdfdes\nfgdsfds",chat_user,"Bot")