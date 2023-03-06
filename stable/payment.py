import uuid

from dotenv import load_dotenv
import os

import time

import json

from goods import Goods, Good

from yookassa import Configuration, Payment

from chat_user import ChatUser

from db_interface import DatabaseInterface

load_dotenv()

Configuration.account_id = os.environ.get("YOOKASSA_ACCOUNT_ID")
Configuration.secret_key = os.environ.get("YOOKASSA_SECRET_KEY")


def create_payment(good:Good, chat_user:ChatUser):

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
        "description": str(good)
    }, uuid.uuid4())

    payment_data = json.loads(payment.json())

    db = DatabaseInterface()


    db.create_payment(payment_data["id"], chat_user.user_id, chat_user.user_name)
    db.close()

    return json.loads(payment.json())

chat_user = ChatUser("name",123321)

url = create_payment(Goods.Tokens.option3,chat_user)

print(url)

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