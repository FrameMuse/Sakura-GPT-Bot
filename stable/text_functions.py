from telebot import types

import re

from behaviors import Behaviors

from chat_user import ChatUser
from chat_gpt import chatGPT
from chat_gpt import get_image


last_message = []

def get_avaliable_behaviours():
    behaviors_dict = {}
    for behavior in Behaviors.__dict__:
        if not behavior.startswith('__') and behavior != "get_names":
            behaviors_dict[Behaviors.__dict__[behavior].name] = Behaviors.__dict__[behavior]

    return behaviors_dict


def on_behaviour_change(message,chat_user: ChatUser,bot,behaviors_dict):
    chat_user.behavior = behaviors_dict[message.text].behaviour
    bot.send_chat_action(message.chat.id, "typing")
    chat_user.clear_message_history()
    message_content = chatGPT("Привет!", chat_user.behavior + " Человека с которым ты общаешься зовут " + message.from_user.first_name , chat_user.messages)
    
    bot.send_message(message.chat.id, message_content)
    
    # Charge tokens for changing behavior.
    chat_user.tokens -= 5
    chat_user.save()


def start_command(message,bot):
    behaviors_list = Behaviors.get_names()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
    buttons = [types.KeyboardButton(name) for name in behaviors_list]
    buttons.append(types.KeyboardButton("👤 Профиль"))
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Привет, я чат-бот Sakura! Я могу вести с тобой диалог, и понимать контекст сказанного тобой!", reply_markup=markup)


def on_profile_button(message,bot,chat_user):
    menu_text = "🌸 Ваш профиль:\n\n🔮 Ваше имя: " + message.from_user.first_name + "\n💰 Ваш баланс токенов: " + str(chat_user.tokens) + "\n📀 Выбранный образ: 🌸 [issue #1]"
    donate_button = types.InlineKeyboardButton(text='🍩 Пополнить баланс', callback_data='donate')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(donate_button)

    bot.send_message(message.chat.id, menu_text, reply_markup=keyboard)


def text(message,bot,chat_user):
    image_url = None
    
    bot.send_chat_action(message.chat.id, "typing")
    message_content = chatGPT(message.text, chat_user.behavior , chat_user.messages)

    result = re.search(r"\!\[(.*?)\]", message_content)

    if result:
        image_description = result.group(1)
        image_url = get_image(image_description)

        message_content = message_content.replace(f'![{result.group(1)}]', "")

    bot.send_message(message.chat.id, message_content,)

    if not image_url:
        bot.send_photo(message.chat.id,photo=image_url)

    chat_user.tokens -= int(len(message.text)/0.75)
    chat_user.add_message("user",message.text)
    chat_user.add_message("assistant",message_content)
    chat_user.save()