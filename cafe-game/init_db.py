import sqlite3

conn = sqlite3.connect('cafe.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE orders
        (order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_name TEXT NOT NULL,
        recipient_name TEXT NOT NULL,
        item_name TEXT NOT NULL,
        message TEXT NOT NULL); ''')

print("Table created successfully")
conn.close()