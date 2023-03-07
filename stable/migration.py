import sqlite3

# Создаем подключение к базе данных
conn = sqlite3.connect('payments.db')

# Создаем курсор для выполнения операций с базой данных
c = conn.cursor()

# Создаем таблицу с указанными колонками
c.execute('''CREATE TABLE IF NOT EXISTS payments
             (id INTEGER PRIMARY KEY,
              uuid TEXT,
              user_id INTEGER,
              user_name TEXT,
              status TEXT,
              tokens INTEGER,
              created_at INTEGER,
              updated_at INTEGER)''')

# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение с базой данных
conn.close()