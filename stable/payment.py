import uuid
import os
import telebot
import json

from dotenv import load_dotenv
from goods import Good, Goods
from yookassa import Configuration, Payment
from yookassa.domain.response import PaymentResponse

from user import User
from db_interface import DatabaseInterface

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

    db = DatabaseInterface()


    db.create_payment(payment_data["id"], user.id, user.username, good)
    db.close()

    return json.loads(payment.json())

def on_success_payment(user: User, credited_tokens: int):
    message = f"""
    🌸 Аввввррр, спасибо мой дорогой друг!
    
    На твой баланс токенов было зачислено {credited_tokens} токенов!
    Теперь у тебя {user.balance} токеньчиков! ❤️
    """

    bot.send_message(user.id, message)

# user = User("name",565324826)
# url = create_payment(Goods.Tokens.option3,user)

# print(url)





# payment = {"amount": {"currency": "RUB", "value": "499.00"}, "confirmation": {"confirmation_url": "https://yoomoney.ru/checkout/payments/v2/contract?orderId=2b984aba-000f-5000-9000-10fe47251494", "type": "redirect"}, "created_at": "2023-03-06T18:54:50.745Z", "description": "3750 Токенов - 499 RUB", "id": "2b984aba-000f-5000-9000-10fe47251494", "metadata": {}, "paid": False, "recipient": {"account_id": "200134", "gateway_id": "2057098"}, "refundable": False, "status": "pending", "test": True}


# payment = Payment.create({
#     "amount": {
#         "value": "69",
#         "currency": "RUB"
#     },
#     "confirmation": {
#       "type": "redirect",
#       "return_url": "https://t.me/sakuraGPTbot"
#     },
#     "capture": True,
#     "description": "Заказ №1"
# }, uuid.uuid4())

# print(payment.json())

# "confirmation": {
#         "type": "",
#         "text": "heooo"
#     },