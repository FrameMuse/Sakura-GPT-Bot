from flask import Flask, request, Request
from flask_sslify import SSLify

import json
from yookassa.domain.notification import WebhookNotification

from db_interface import DatabaseInterface, PaymentStatus
import os
from dotenv import load_dotenv
from payment import on_success_payment

app = Flask(__name__)
sslify = SSLify(app)

load_dotenv()
WEBHOOK_ROUTE = str(os.environ.get("WEBHOOK_ROUTE"))


def parse_payment(payload):
    # Cоздайте объект класса уведомлений в зависимости от события
    try:
        notification_object = WebhookNotification(json.loads(payload))
        # Получите объекта платежа
        payment = notification_object.object
        if not payment:
            raise Exception("Pizdoc")
        
        # print(payment.id)
        # print(payment.status)
        return payment
    except Exception as error:
        # обработка ошибок
        print(error)



@app.route(WEBHOOK_ROUTE, methods=['POST'])
def webhook():
    payment = parse_payment(request.data)
    if not payment:
        return 'Payment is null.', 400

    print(payment.status == "succeeded")
    print(payment.paid)

    if payment.status == "succeeded" and payment.paid:
        try:
            db = DatabaseInterface()
            db.set_status(payment.id, PaymentStatus.SUCCEEDED)

            payment_entry = db.select_data(payment.id)
            user_id = payment_entry[2]
            user_name = payment_entry[3]
            tokens = payment_entry[5]

            print(user_id, user_name, tokens)
            on_success_payment(user_name, user_id, tokens)

            db.close()
        except Exception as error:
            print(error)
        
        return 'success', 200
    
    return 'Unknown error.', 400

if __name__ == '__main__':
    app.run(
        port=443,
        host="95.163.236.117",
        ssl_context=('ssl/certificate.crt', 'ssl/private.key'),
        # debug=True
    )







# from yookassa import Configuration, Webhook

# import os
# from dotenv import load_dotenv

# load_dotenv()

# Configuration.account_id = os.environ.get("YOOKASSA_ACCOUNT_ID")
# Configuration.secret_key = os.environ.get("YOOKASSA_SECRET_KEY")

# # Configuration.configure_auth_token('<Bearer Token>')

# response = Webhook.add({
#     "event": "payment.succeeded",
#     "url": "https://sakurachat.space/payment-e4808a6e-a824-45fe-a43a-adb43c050054",
# })

# print(response)