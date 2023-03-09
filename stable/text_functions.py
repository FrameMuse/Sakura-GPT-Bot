from telebot import TeleBot
from telebot import types

import re

from personalities import Personalities

from user import User
from chat_gpt import chatGPT
from chat_gpt import get_image

from logger import log_text

last_message = []


def on_behaviour_change(bot: TeleBot, user: User, text: str):
    user.personality = Personalities.find_by_title(text)
    # Modify behaviour.
    user.personality.behaviour += " Человека с которым ты общаешься зовут " + user.first_name

    bot.send_chat_action(user.id, "typing")
    message_content = chatGPT("Привет!", user.personality, user.message_history.get())

    image_pattern = r"\!\[(.*?)\]"
    message_content = re.sub(image_pattern, "", message_content)
    
    bot.send_message(user.id, message_content)


def on_profile_button(bot: TeleBot, user: User):
    menu_text = f"""
🌸 Ваш профиль:

🔮 Ваше имя: {user.first_name}
💰 Ваш баланс токенов: {str(int(user.balance.amount))}
📀 Выбранный образ: {user.personality.title}
    """

    donate_button = types.InlineKeyboardButton(text="🍩 Пополнить баланс", callback_data="donate")
    daily_button = types.InlineKeyboardButton(text="🗓️ Ежедневные токены", callback_data="daily")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(donate_button)
    keyboard.add(daily_button)

    bot.send_message(user.id, menu_text, reply_markup=keyboard)


def text(bot: TeleBot, user: User, user_message: str):
    log_text(user_message, user, user.message_history.Role.USER)

    bot.send_chat_action(user.id, "typing")

    try:
        assistant_message = chatGPT(user_message, user.personality, user.message_history.get())
        assistant_message.lower()
        
        if len(assistant_message) > 4096:
            raise Exception(":C")
    except:
        bot.send_message(user.id, "⚙️ Не удалось синтезировать ответ.")
        return

    log_text(assistant_message, user, user.message_history.Role.ASSISTANT)
    user.balance.debit_chars(len(user_message))


    image_url = None
    image_pattern = r"\!\[(.*?)\]"
    
    result = re.search(image_pattern, assistant_message)
    if result:
        image_description = result.group(1)

        try:
            image_url = get_image(image_description)

            user.balance.debit(15)
            user.balance.debit_chars(len(image_description) / 5)

        except openai.error.InvalidRequestError:  # type: ignore
            bot.send_message(user.id, "⚙️ Не удалось сгенерировать изображение :C")
            
        # Change message_content if there is a link.
        assistant_message = re.sub(image_pattern, "", assistant_message)

    user.message_history.add(user.message_history.Role.USER,      user_message)
    user.message_history.add(user.message_history.Role.ASSISTANT, assistant_message)

    bot.send_message(user.id, assistant_message)

    if image_url != None:
        bot.send_photo(user.id,photo=image_url)
    
