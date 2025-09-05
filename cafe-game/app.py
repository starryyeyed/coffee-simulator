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

# main route for starting screen
@app.route('/select_blend', methods=['POST'])
def blend():
    return render_template('blend.html')

# route that displays all previous orders
@app.route('/orders')
def show_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

# routes for the coffee-making steps
@app.route('/select_roast', methods=['POST'])
def select_roast():
    bean_blend = request.form.get('bean_blend')
    return render_template('roast.html', bean_blend=bean_blend)

@app.route('/select_temperature', methods=['POST'])
def select_temperature():
    bean_blend = request.form.get('bean_blend')
    roast_type = request.form.get('roast_type')
    return render_template('temperature.html', bean_blend=bean_blend, roast_type=roast_type)

@app.route('/message', methods=['POST'])
def message():
    bean_blend = request.form['bean_blend']
    roast_type = request.form['roast_type']
    temperature = request.form['temperature']
    return render_template('message_prompt.html', bean_blend=bean_blend, roast_type=roast_type, temperature=temperature)

@app.route('/complete_order', methods=['POST'])
def complete_order():
    # Retrieve all the selections from the form
    bean_blend = request.form['bean_blend']
    roast_type = request.form['roast_type']
    temperature = request.form['temperature']
    
    sender_name = request.form['sender_name']
    recipient = request.form['recipient']
    message = request.form['message']

    # Generate a custom drink name based on the choices
    drink_name = f"{temperature} {roast_type} {bean_blend}"

    # Insert the final order into the database
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO orders (item_name, price, message, sender_name, recipient) VALUES (?, ?, ?, ?, ?)',
        (drink_name, 5.00, message, sender_name, recipient)
    )
    conn.commit()
    conn.close()

    # Create a summary dictionary to display on the summary page
    order_summary = {
        'drink_name': drink_name,
        'message': message,
        'sender_name': sender_name,
        'recipient': recipient
    }

    return render_template('summary.html', order_summary=order_summary)


if __name__ == '__main__':
    app.run(debug=True)