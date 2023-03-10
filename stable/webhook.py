from flask import Flask, request, Request
from flask_sslify import SSLify

import json
from yookassa.domain.notification import WebhookNotification

from db.repositories.payments import PaymentsRepository
import os
from dotenv import load_dotenv
from payment import on_success_payment
from user import User

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



@app.route(WEBHOOK_ROUTE, methods=["POST"])
def webhook():
    payment = parse_payment(request.data)
    if not payment:
        return "Payment is null.", 400

    print(payment.status == "succeeded")
    print(payment.paid)

    if payment.status == "succeeded" and payment.paid:
        repository = PaymentsRepository()
        
        try:
            repository.set_status(str(payment.id), repository.Status.SUCCEEDED)

            payment = repository.find(str(payment.id))
            if not payment:
                raise Exception("No payment found.")

            user = User(int(payment.user_id))
            print(user.id, user.username, payment.tokens)
            on_success_payment(user, int(payment.tokens))

            repository.close()
            return "success", 200
        except Exception as error:
            print(error)
            repository.close()
            return str(error), 400
    
    return "Unknown error.", 400

if __name__ == "__main__":
    app.run(
        port=443,
        host="95.163.236.117",
        ssl_context=("ssl/certificate.crt", "ssl/private.key"),
        # debug=True
    )







# from yookassa import Configuration, Webhook

# import os
# from dotenv import load_dotenv

# load_dotenv()

# Configuration.account_id = os.environ.get("YOOKASSA_ACCOUNT_ID")
# Configuration.secret_key = os.environ.get("YOOKASSA_SECRET_KEY")

# # Configuration.configure_auth_token("<Bearer Token>")

# response = Webhook.add({
#     "event": "payment.succeeded",
#     "url": "https://sakurachat.space/payment-e4808a6e-a824-45fe-a43a-adb43c050054",
# })

# print(response)