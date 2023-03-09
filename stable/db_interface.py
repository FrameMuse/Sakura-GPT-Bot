import sqlite3

from enum import Enum
from goods import Good

import time

class PaymentStatus(Enum):
    CREATED = 1
    SUCCEEDED = 2

class DatabaseInterface:
    def __init__(self, db_file="payments.db"):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def create_payment(self, uuid, user_id, username, good: Good):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        self.cursor.execute('''INSERT INTO payments (uuid, user_id, user_name, status, tokens, created_at, updated_at)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', (uuid, user_id, username, PaymentStatus.CREATED.name, good.quantity, timestamp, timestamp))
        self.connection.commit()


    def select_data(self, uuid):
        self.cursor.execute(f'''SELECT * FROM payments WHERE uuid="{uuid}"''')
        return self.cursor.fetchone()


    def set_status(self, uuid, status:PaymentStatus):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        self.cursor.execute('''UPDATE payments SET status=?, updated_at=?
                          WHERE uuid=?''', (status.name, timestamp, uuid))
        self.connection.commit()


    def close(self):
        self.connection.close()


# db = DatabaseInterface()

# db.create_payment('12345', 1, 'John')
# db.create_payment('64524', 2, 'John')
# db.set_paid('12345')

# db.set_status('12345',PaymentStatus.SUCCEEDED)

# print(db.select_data("2b988180-000f-5000-a000-15923964c419")[5])

# db.close()