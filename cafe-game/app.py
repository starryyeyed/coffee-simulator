from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cafe.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orders')
def show_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/place-order', methods=['POST'])
def place_order():
    item_name = request.form['item_name']
    sender_name = request.form['sender_name']
    recipient = request.form['recipient_name']
    message = request.form['message']

    conn = get_db_connection()
    conn.execute('INSERT INTO orders (item_name, sender_name, recipient_name, message) VALUES (?, ?, ?, ?)',
                 (item_name, sender_name, recipient, message))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/start_game', methods=['POST'])
def start_game():
    # Add your game starting logic here
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)