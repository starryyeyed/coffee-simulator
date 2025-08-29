from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def handle_order():  # processes new order
    order_data = request.json
    print("New order:", order_data)

    # with sqlite3.connect('cafe.db') as conn:
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO orders (item, date) VALUES (?, ?)", (order_data['item'], order_data['time']))
        # conn.commit()
    return{'status': 'success'}

if __name__ == '__main__':
    app.run(debug=True)