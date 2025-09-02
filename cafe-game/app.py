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

@app.route('/select_add_ons', methods=['POST'])
def select_milk():
    bean_blend = request.form.get('bean_blend')
    roast_type = request.form.get('roast_type')
    temperature_type = request.form.get('temperature_type')
    return render_template('add_ons.html', bean_blend=bean_blend, roast_type=roast_type, temperature_type=temperature_type)

@app.route('/final_prompt', methods=['POST'])
def final_prompt():
    bean_blend = request.form.get('bean_blend')
    roast_type = request.form.get('roast_type')
    temperature_type = request.form.get('temperature_type')
    add_ons = request.form.getlist('add_ons')
    
    drink_name=f"{temperature_type} {roast_type} {bean_blend} {add_ons}"

    return render_template('message_prompt.html', drink_name=drink_name)

# adding order to a database
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
    return redirect(url_for('orders'))

if __name__ == '__main__':
    app.run(debug=True)