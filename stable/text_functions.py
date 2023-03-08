from telebot import types

import re

from time import time

from behaviors import Personalities

from chat_user import ChatUser
from chat_gpt import chatGPT
from chat_gpt import get_image

from logger import log_text

last_message = []

def get_avaliable_behaviours():
    personalities_dict = {}
    for property in Personalities.__dict__:
        if not property.startswith('__') and property != "get_names" and property != "find" and property != "find_by_title":
            personality = Personalities.find(property)
            personalities_dict[personality.title] = personality.behaviour

    return personalities_dict


def on_behaviour_change(message, chat_user: ChatUser, bot):
    chat_user.personality = Personalities.find_by_title(message.text)
    chat_user.clear_message_history()
    chat_user.save()
    # Modify behaviour.
    chat_user.personality.behaviour += " Человека с которым ты общаешься зовут " + message.from_user.first_name

    bot.send_chat_action(message.chat.id, "typing")
    message_content = chatGPT("Привет!", chat_user.personality, chat_user.messages)

    image_pattern = r"\!\[(.*?)\]"
    message_content = re.sub(image_pattern, "", message_content)
    
    bot.send_message(message.chat.id, message_content)


# def start_command(message,bot):
#     behaviors_list = Personalities.get_names()
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
#     buttons = [types.KeyboardButton(name) for name in behaviors_list]
#     buttons.append(types.KeyboardButton("👤 Профиль"))
#     markup.add(*buttons)

#     bot.send_message(message.chat.id, "Привет, я чат-бот Sakura! Я могу вести с тобой диалог, и понимать контекст сказанного тобой!", reply_markup=markup)


def on_profile_button(message,bot,chat_user: ChatUser):
    menu_text = "🌸 Ваш профиль:\n\n🔮 Ваше имя: " + message.from_user.first_name + "\n💰 Ваш баланс токенов: " + str(chat_user.tokens) + f"\n📀 Выбранный образ: {chat_user.personality.title}"
    donate_button = types.InlineKeyboardButton(text='🍩 Пополнить баланс', callback_data='donate')
    daily_button = types.InlineKeyboardButton(text='🗓️ Ежедневные токены', callback_data='daily')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(donate_button)
    keyboard.add(daily_button)

    bot.send_message(message.chat.id, menu_text, reply_markup=keyboard)


def text(message, bot, chat_user: ChatUser):
    log_text(message.text,chat_user,"User")
    bot.send_chat_action(message.chat.id, "typing")
    try:
        message_content = chatGPT(message.text, chat_user.personality , chat_user.messages)
        message_content.lower()
        if len(message_content) > 4096:
            raise Exception(":C")
    except:
        bot.send_message(message.chat.id, "⚙️ Не удалось синтезировать ответ.")
        return
    log_text(message_content,chat_user)
    chat_user.tokens -= int(len(message.text)/0.75)
    chat_user.save()


    image_url = None
    image_pattern = r"\!\[(.*?)\]"
    
    result = re.search(image_pattern, message_content)


    if result:
        image_description = result.group(1)
        try:
            image_url = get_image(image_description)
        except openai.error.InvalidRequestError:  # type: ignore
            bot.send_message(message.chat.id, "⚙️ Не удалось сгенерировать изображение :C")
            

        message_content = re.sub(image_pattern, "", message_content)

    bot.send_message(message.chat.id, message_content)

    if image_url != None:
        bot.send_photo(message.chat.id,photo=image_url)
    
    
    

    chat_user.add_message("user",message.text)
    chat_user.add_message("assistant",message_content)
    chat_user.save()
