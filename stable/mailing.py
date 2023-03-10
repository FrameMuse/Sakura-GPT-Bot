import os
import telebot
from telebot import types

path = 'user-data'

user_ids = [int(f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

from dotenv import load_dotenv
import os

load_dotenv()
token = os.environ.get("TELEGRAM_KEY")

bot = telebot.TeleBot(str(token))

class ButtonTypes:
    LINK = "link"
    CALLBACK = "callback"

class Mail:
    
    def __init__(self,text:str,button:bool, type, button_text="", button_callback_data="", button_link=""):
        self.text = text
        if not button:
            return
        
        self.contain_button = button

        self.keyboard = types.InlineKeyboardMarkup()

        if type == "callback":
            self.keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=button_callback_data))
        if type == "link":
            self.keyboard.add(types.InlineKeyboardButton(text=button_text, url=button_link))
        
    def send(self,bot:telebot.TeleBot, uid:int):
        if not self.contain_button:
            bot.send_message(uid, self.text,disable_notification=True)
        else:
            bot.send_message(uid, self.text, reply_markup=self.keyboard,disable_notification=True)
        

# message_text = "❗️Если у вас закончатся токены, то вы можете пополнить баланс, нажав на кнопку ниже❗️"
# keyboard = types.InlineKeyboardMarkup()
# donate_button = types.InlineKeyboardButton(text='🍩 Пополнить баланс', callback_data='donate')
# keyboard.add(donate_button)

mail = Mail(text="🥰Подпишитесь пожалуйста на наш телеграмм канал с новостями связанными с ботом, что бы ничего не упустить!🌸",
            button=True,
            type=ButtonTypes.LINK,
            button_text="🌸Нажмите что-бы перейти🌸",
            button_link="https://t.me/SakuraDevBlog")

block_counter = 0
sent_counter = 0
for user_id in user_ids:
    try:
        mail.send(bot,user_id)
        print("Sent message to " + str(user_id))
        sent_counter+=1
    except:
        block_counter+=1
        print("Error occured while sending message to " + str(user_id))

print(f"Mailing finished\nsent:{sent_counter}\nblocked:{block_counter}")
