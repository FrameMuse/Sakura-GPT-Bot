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

message_text = "❗️Если у вас закончатся токены, то вы можете пополнить баланс, нажав на кнопку ниже."
keyboard = types.InlineKeyboardMarkup()
donate_button = types.InlineKeyboardButton(text='🍩 Пополнить баланс', callback_data='donate')
keyboard.add(donate_button)

for user_id in user_ids:
    try:
        bot.send_message(user_id,message_text,reply_markup=keyboard)
        print("Sent message to " + str(user_id))
    except:
        print("Error occured while sending message to " + str(user_id))


