from placeholders import Placeholders
import openai
import telebot
from telebot import types

import openai

from personalities import Personalities

from user import User
from goods import Goods, Good

from text_functions import on_behaviour_change, on_profile_button,text

from dotenv import load_dotenv
import os

from payment import create_payment
from db.repositories.promocodes import PromocodesRepository

from threading import Thread

load_dotenv()
openai.api_key = os.environ.get("OPEN_AI_KEY")
token = os.environ.get("TELEGRAM_KEY")

bot = telebot.TeleBot(str(token))

regex = r"\[image description: (.*?)]"


admins_uids = [494405580, 565324826]

### --- Commands Handlers --- ###

@bot.message_handler(commands=["start"])
def start_command(message: types.Message):
    User.from_telebot(message.from_user)
    personality_titles = Personalities.avaliable().keys()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
    buttons = [types.KeyboardButton(title) for title in personality_titles]
    buttons.append(types.KeyboardButton("👤 Профиль"))
    markup.add(*buttons)

    bot.send_message(message.chat.id, Placeholders.START_MESSAGE, reply_markup=markup)


@bot.message_handler(commands=["add_promo"])
def add_promo_command(message:types.Message):
    if message.from_user.id not in admins_uids:
        return
    
    repository = PromocodesRepository()

    try:
        repository.add(str(message.text).split(" ")[1],int(str(message.text).split(" ")[2]))
        bot.send_message(message.chat.id,"Succesfully added promocode!")
        return
    except Exception as error:
        bot.send_message(message.chat.id, "Error occured while adding promocode!. " + str(error))
        return
    

@bot.message_handler(commands=["remove_promo"])
def remove_promo_command(message:types.Message):
    if message.from_user.id not in admins_uids:
        return
    
    repository = PromocodesRepository()

    try:
        repository.remove(str(message.text).split(" ")[1])
        bot.send_message(message.chat.id,"Succesfully removed promocode!")
        return
    except Exception as error:
        bot.send_message(message.chat.id, "Error occured while removing promocode!. " + str(error))
        return


@bot.message_handler(commands=["promo"])
def promo_command(message: types.Message):
    user = User.from_telebot(message.from_user)
    code = str(message.text).split(" ")[1]

    if user.promocodes.applied(code):
        bot.send_message(message.chat.id, "Данный промокод уже был активирован" )
        return

    promocode = user.promocodes.find(code)
    if not promocode:
        bot.send_message(message.chat.id, "Данного промокода не существует" )
        return
    
    user.promocodes.apply(code)
    bot.send_message(message.chat.id, "Вы успешно активировали промокод на " + str(promocode.tokens) + " токенов" )

### --- Callback Handlers --- ###

@bot.callback_query_handler(func=lambda call: call.data == "daily")
def on_daily_callback(call: types.CallbackQuery):
    user = User.from_telebot(call.from_user)

    if user.daily_tokens.available():
        obtained_tokens = user.daily_tokens.obtain()
        bot.send_message(call.message.chat.id, f"На счет зачислено {obtained_tokens} токенов!")
    else:
        bot.send_message(call.message.chat.id, "Сегодня вы уже получили ежедневные токены")

    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_tokens:"))
def on_buy_tokens_callback(call: types.CallbackQuery):
    user = User.from_telebot(call.from_user)
    option = call.data.replace("buy_tokens:", "")

    good: Good = Goods.Tokens.__dict__["option" + option]
    good_description = f'🌸Счёт на оплату токенов.\n\nПосле оплаты, вы получите {good.quantity} токенов'

    if user.balance.limit_exceeded(good.quantity):
        bot.send_message(call.message.chat.id, "Извините, но вы достигли лимита токенов :<")
        bot.answer_callback_query(callback_query_id=call.id)
        return

    payment = create_payment(user, good)
    if not payment["confirmation"]:
        raise ValueError("No 'confirmation' in 'payment'.")
    
    confirmation_url = payment["confirmation"]["confirmation_url"]
    pay_button = types.InlineKeyboardButton(f"Оплатить {good.price} {good.currency}", confirmation_url)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(pay_button)

    bot.send_message(call.message.chat.id, good_description, reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: call.data == "donate")
def on_donate_callback(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()

    for property in Goods.Tokens.__dict__:
        if not property.startswith("option"): continue

        good: Good = Goods.Tokens.__dict__[property]
        callback_data = "buy_tokens:" + property.replace("option", "")
        button = types.InlineKeyboardButton(str(good), callback_data=callback_data)
        keyboard.add(button)

    message_content = """ 
    🌸Вот список моих товаров.\n\n📖 Выберите подходящий для вас вариант:
    """
    bot.send_message(call.message.chat.id, message_content, reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=call.id)

### --- Message Handlers --- ###

@bot.message_handler(content_types=["text"])
def texts(message: types.Message):
    if not message.text: return

    user = User.from_telebot(message.from_user)

    if message.text == "👤 Профиль":
       on_profile_button(bot, user)
       return
    
    if not user.balance.sufficient_chars(len(message.text)):
        donate_button = types.InlineKeyboardButton(text='🍩 Пополнить баланс', callback_data='donate')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(donate_button)
        bot.send_message(message.chat.id, f"""
Уууппс, у тебя недостаточно токенов для отправки сообщения!
Твой баланс токенов равен: {str(int(user.balance.amount))}
""", reply_markup=keyboard)
        return

    if Personalities.has(message.text):
        on_behaviour_change(bot, user, message.text)
        return

    Thread(target=text,args=(bot,user,message.text)).start()
    
@bot.message_handler(content_types=["sticker"])
def on_sticker_sent(message: types.Message):
    if not message.sticker: return
    
    user = User.from_telebot(message.from_user)
    
    Thread(target=text,args=(bot, user, message.sticker.emoji)).start()

bot.infinity_polling()
