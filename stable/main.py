import time

from placeholders import Placeholders
import openai
import telebot
from telebot import types

import openai

import re

from behaviors import Personalities

from goods import Goods, Good

from chat_user import ChatUser
from chat_gpt import chatGPT
from chat_gpt import get_image

from text_functions import get_avaliable_behaviours,on_behaviour_change,on_profile_button,text

from voice import collect_garbage, ogg_to_wav, recognize, text_to_speech

from dotenv import load_dotenv
import os


load_dotenv()
openai.api_key = os.environ.get("OPEN_AI_KEY")
token = os.environ.get("TELEGRAM_KEY")
TELEGRAM_INVOICE_PROVIDER_TOKEN = os.environ.get("TELEGRAM_INVOICE_PROVIDER_TOKEN")

bot = telebot.TeleBot(str(token))

last_message = []

regex = r"\[image description: (.*?)]"



@bot.message_handler(commands=["start"])
def start_command(message):

    behaviors_list = Personalities.get_names()
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
    buttons = [types.KeyboardButton(name) for name in behaviors_list]
    buttons.append(types.KeyboardButton("👤 Профиль"))
    markup.add(*buttons)

    bot.send_message(message.chat.id, Placeholders.START_MESSAGE , reply_markup=markup)

@bot.pre_checkout_query_handler(func=lambda call: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    # Отправляем запрос на проверку счета
    # print(pre_checkout_query.order_info)
    bot.answer_pre_checkout_query(int(pre_checkout_query.id), ok=True)



@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call: types.CallbackQuery):
    if call.data.startswith("buy_tokens:"):
        option = call.data.replace("buy_tokens:", "")
        good: Good = Goods.Tokens.__dict__["option" + option]

        good_description = f'🌸Счёт на оплату токенов.\n\nПосле оплаты, вы получите {good.quantity} токенов'
        good_price = types.LabeledPrice(str(good.price), good.price * 100)

        if not TELEGRAM_INVOICE_PROVIDER_TOKEN:
            return

        bot.send_invoice(
            call.message.chat.id,
            title='Счёт',
            description=good_description, 
            invoice_payload=str(good.quantity),
            provider_token=TELEGRAM_INVOICE_PROVIDER_TOKEN,
            currency=good.currency,
            prices=[good_price]
        )
        bot.answer_callback_query(callback_query_id=call.id)

    if call.data == "donate":
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text=str(Goods.Tokens.option1),callback_data="buy_tokens:1")
        button2 = types.InlineKeyboardButton(text=str(Goods.Tokens.option2),callback_data="buy_tokens:2")
        button3 = types.InlineKeyboardButton(text=str(Goods.Tokens.option3),callback_data="buy_tokens:3")
        for button in [button1, button2, button3]:
            keyboard.add(button)

        message_content = """ 
        🌸Вот список моих товаров.\n\n📖 Выберите подходящий для вас вариант:
        """
        bot.send_message(call.message.chat.id, message_content, reply_markup=keyboard)
        bot.answer_callback_query(callback_query_id=call.id)


@bot.message_handler(content_types=["text"])
def texts(message):
    chat_user = ChatUser(message.from_user.id)
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
    chat_user = ChatUser(message.from_user.id)
    chat_user.restore_message_history()

    bot.send_chat_action(message.chat.id, "typing")
    message_content = chatGPT(message.text, chat_user.personality, chat_user.messages)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=last_message[-1].id, text=message_content)


@bot.message_handler(content_types=["voice"])
def voice(message):
    chat_user = ChatUser(message.from_user.id)
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

@bot.message_handler(commands=["image"])
def image_command(message):
    try:
        response = openai.Image.create(
            prompt=message.text,
            n=1,
            size="1024x1024"
        )
    except openai.error.InvalidRequestError:  # type: ignore
        bot.send_message(message.chat.id, "*****, нельзя такое")
        return

    image_url = response['data'][0]['url']  # type: ignore

    bot.send_message(message.chat.id, image_url)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    tokens = int(message.successful_payment.invoice_payload)

    chat_user = ChatUser(message.from_user.id)
    chat_user.restore_settings()

    chat_user.tokens += tokens
    chat_user.save()
    

    image_link = get_image("Anime girl Sakura, the most cutest. Icon for telegram with a background.")
    
    bot.send_message(message.chat.id, f'🌸 Аввввррр, спасибо мой дорогой друг!\n\nНа твой баланс токенов было зачислено {tokens} токенов!')
    bot.send_photo(message.chat.id, photo=image_link)



bot.infinity_polling()
