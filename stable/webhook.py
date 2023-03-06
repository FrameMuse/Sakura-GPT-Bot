from flask import Flask, request
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

@app.route('/payment', methods=['POST'])
def payment_post():
    name = request.form.get('name')
    return f'Hello world, {name}!'

@app.route('/payment-e4808a6e-a824-45fe-a43a-adb43c050054', methods=['GET'])
def payment_get():
    return f'Hello world!'

if __name__ == '__main__':
    app.run(port=443,host="95.163.236.117")

