from telebot import TeleBot
from telebot import types

from personalities import Personalities

from user import User
from chat_gpt import chatGPT

from logger import log_text

last_message = []



def on_behaviour_change(bot: TeleBot, user: User, text: str):
    user.personality = Personalities.find_by_title(text)
    # Modify behaviour.
    user.personality.behaviour += " Человека с которым ты общаешься зовут " + user.first_name

    bot.send_chat_action(user.id, "typing")
    message_content = chatGPT("Привет!", user.personality, user.message_history.get())

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

PROMPT_CHARS_LIMIT = 250

def text(bot: TeleBot, user: User, user_message: str):
    # log_text(user_message, user, user.message_history.Role.USER)

    bot.send_chat_action(user.id, "typing")

    # Limit user message length.
    if len(user_message) > PROMPT_CHARS_LIMIT:
        user_message = user_message[:PROMPT_CHARS_LIMIT]

    try:
        assistant_message = chatGPT(user_message, user.personality, user.message_history.get())
        assistant_message.lower()
        
        if len(assistant_message) > 4096:
            raise Exception(":C")
    except:
        bot.send_message(user.id, "⚙️ Не удалось синтезировать ответ.")
        return

    # log_text(assistant_message, user, user.message_history.Role.ASSISTANT)
    user.balance.debit_chars(len(user_message))

    user.message_history.add(user.message_history.Role.USER,      user_message)
    user.message_history.add(user.message_history.Role.ASSISTANT, assistant_message)

    bot.send_message(user.id, assistant_message)
