import sqlite3

from enum import Enum

import time

class PaymentStatus(Enum):
    SUCCEEDED = 1
    PENDING = 2
    REFUND = 3
    CANCELED = 4

class DatabaseInterface:
    def __init__(self, db_file="payments.db"):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def create_payment(self, uuid, user_id, user_name):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        self.cursor.execute('''INSERT INTO payments (uuid, user_id, user_name, status, created_at, updated_at)
                          VALUES (?, ?, ?, ?, ?, ?)''', (uuid, user_id, user_name,  PaymentStatus.PENDING.name , timestamp, None))
        self.connection.commit()


    def select_data(self):
        self.cursor.execute('''SELECT * FROM payments''')
        return self.cursor.fetchall()


    def set_status(self, uuid, status:PaymentStatus):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        self.cursor.execute('''UPDATE payments SET status=?, updated_at=?
                          WHERE uuid=?''', (status.name, timestamp, uuid))
        self.connection.commit()


    def close(self):
        self.connection.close()


db = DatabaseInterface()

db.create_payment('12345', 1, 'John')
# db.set_paid('12345')

db.set_status('12345',PaymentStatus.CANCELED)

db.close()