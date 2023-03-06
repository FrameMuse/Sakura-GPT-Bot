import time

from placeholders import Placeholders
import openai
import telebot
from telebot import types

import openai

from behaviors import Personalities

from goods import Goods, Good

from chat_user import ChatUser
from chat_gpt import chatGPT

from text_functions import get_avaliable_behaviours,on_behaviour_change,on_profile_button,text

from voice import collect_garbage, ogg_to_wav, recognize, text_to_speech

from dotenv import load_dotenv
import os

from payment import create_payment


load_dotenv()
openai.api_key = os.environ.get("OPEN_AI_KEY")
token = os.environ.get("TELEGRAM_KEY_TEST")

bot = telebot.TeleBot(str(token))

last_message = []

regex = r"\[image description: (.*?)]"



@bot.message_handler(commands=["start"])
def start_command(message):
    chat_user = ChatUser(message.from_user.username, message.from_user.id)
    chat_user.restore_settings()
    chat_user.user_chat_id = message.chat.id
    chat_user.save()


    behaviors_list = Personalities.get_names()
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
    buttons = [types.KeyboardButton(name) for name in behaviors_list]
    buttons.append(types.KeyboardButton("👤 Профиль"))
    markup.add(*buttons)

    bot.send_message(message.chat.id, Placeholders.START_MESSAGE , reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call: types.CallbackQuery):
    if call.data.startswith("buy_tokens:"):
        option = call.data.replace("buy_tokens:", "")

        good: Good = Goods.Tokens.__dict__["option" + option]
        good_description = f'🌸Счёт на оплату токенов.\n\nПосле оплаты, вы получите {good.quantity} токенов'

        chat_user = ChatUser(call.from_user.username, call.from_user.id)
        chat_user.restore_settings()

        # TODO: CREATE_PAYMENT
        payment = create_payment(good, chat_user)
        if not payment["confirmation"]:
            raise ValueError("No 'confirmation' in 'payment'.")
        
        button_pay = types.InlineKeyboardButton(text=f"Оплатить {good.price} {good.currency}", url=payment["confirmation"]["confirmation_url"])

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_pay)

        bot.send_message(call.message.chat.id, good_description, reply_markup=keyboard)
        bot.answer_callback_query(callback_query_id=call.id)

    if call.data == "donate":
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text=str(Goods.Tokens.option1), callback_data="buy_tokens:1")
        button2 = types.InlineKeyboardButton(text=str(Goods.Tokens.option2), callback_data="buy_tokens:2")
        button3 = types.InlineKeyboardButton(text=str(Goods.Tokens.option3), callback_data="buy_tokens:3")
        for button in [button1, button2, button3]:
            keyboard.add(button)

        message_content = """ 
        🌸Вот список моих товаров.\n\n📖 Выберите подходящий для вас вариант:
        """
        bot.send_message(call.message.chat.id, message_content, reply_markup=keyboard)
        bot.answer_callback_query(callback_query_id=call.id)


# @bot.message_handler(commands=["image"])
# def image_command(message):
#     try:
#         response = openai.Image.create(
#             prompt=message.text,
#             n=1,
#             size="1024x1024"
#         )
#     except openai.error.InvalidRequestError:  # type: ignore
#         bot.send_message(message.chat.id, "*****, нельзя такое")
#         return

#     image_url = response['data'][0]['url']  # type: ignore

#     bot.send_message(message.chat.id, image_url)


@bot.message_handler(content_types=["text"])
def texts(message):
    chat_user = ChatUser(message.from_user.username,message.from_user.id)
    chat_user.restore_message_history()
    chat_user.restore_settings()

    if message.text == "👤 Профиль":
       on_profile_button(message,bot,chat_user)
       return
    

    if chat_user.tokens < int(len(message.text)/0.75):
        bot.send_message(message.chat.id, "Уууппс, у тебя недостаточно токенов для отправки сообщения! Твой баланс токенов равен: "+str(chat_user.tokens))
        chat_user.save()
        return

    behaviors_dict = get_avaliable_behaviours()
    if message.text in behaviors_dict:
        on_behaviour_change(message,chat_user, bot)
        return
    
    
    text(message, bot, chat_user)
    

@bot.edited_message_handler(func=lambda message: True)
def edit_text(message):
    chat_user = ChatUser(message.from_user.username, message.from_user.id)
    chat_user.restore_message_history()

    bot.send_chat_action(message.chat.id, "typing")
    message_content = chatGPT(message.text, chat_user.personality, chat_user.messages)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=last_message[-1].id, text=message_content)


@bot.message_handler(content_types=["voice"])
def voice(message):
    chat_user = ChatUser(message.from_user.username,message.from_user.id)
    chat_user.restore_message_history()
    
    # display "typing" status bar
    bot.send_chat_action(message.chat.id, "typing")

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_name = str(time.time()) + "-voice.ogg"
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    ogg_to_wav(file_name)
    text = recognize(file_name.replace(".ogg", ".wav"))
    chat_user.add_message("user",str(text))
    
    sent_message = bot.send_message(message.chat.id, str(text))

    bot.send_chat_action(message.chat.id, "typing")

    message_content = chatGPT(text, chat_user.personality, chat_user.messages)
    chat_user.add_message("assistant",message_content)

    bot.reply_to(sent_message, message_content)

    bot.send_chat_action(message.chat.id, "record_audio")
    speech_file_name = text_to_speech(message_content)
    speech_file = open(speech_file_name, "rb")

    bot.send_chat_action(message.chat.id, "upload_audio")
    bot.send_voice(message.chat.id, speech_file,
                   reply_to_message_id=sent_message.id)

    chat_user.save()
    collect_garbage([file_name, file_name.replace(
        ".ogg", ".wav"), speech_file_name])

bot.infinity_polling()
