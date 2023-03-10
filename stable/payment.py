import uuid
import os
import telebot
import json

from dotenv import load_dotenv
from goods import Good
from yookassa import Configuration, Payment

from db.repositories.payments import PaymentsRepository

from user import User

load_dotenv()

Configuration.account_id = os.environ.get("YOOKASSA_ACCOUNT_ID")
Configuration.secret_key = os.environ.get("YOOKASSA_SECRET_KEY")

token = os.environ.get("TELEGRAM_KEY")
bot = telebot.TeleBot(str(token))


def create_payment(user: User, good: Good):
    payment = Payment.create({
        "amount": {
            "value": good.price,
            "currency": good.currency
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/sakuraGPTbot"
        },
        "capture": True,
        "description": str(good),
        "metadata": {
            "user_id": user.id,
            "first_name": user.first_name,
        }
    }, uuid.uuid4())

    payment_data = json.loads(payment.json())

    repository = PaymentsRepository()
    repository.create(payment_data["id"], user.id, good.quantity)
    repository.close()

    return json.loads(payment.json())

def on_success_payment(user: User, tokens: int):
    user.balance.credit(tokens)
    
    message = f"""
🌸 Аввввррр, спасибо мой дорогой друг!

На твой баланс токенов было зачислено {tokens} токенов!
Теперь у тебя {user.balance} токеньчиков! ❤️
"""

    bot.send_message(user.id, message)
