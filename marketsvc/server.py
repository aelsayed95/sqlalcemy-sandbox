import os
from flask import Flask, jsonify, request

from db_accessor import get_customers, get_orders_of_customer, get_total_cost_of_an_order, get_orders_between_dates

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Welcome to MarketPlace!</h1>"

@app.route('/api/customers')
def customers():
    return jsonify(get_customers())

@app.route('/api/orders')
def orders():
    cust_id = request.args.get('cust_id')
    return jsonify(get_orders_of_customer(cust_id))

@app.route('/api/order_total')
def order_total():
    order_id = request.args.get('order_id')
    return jsonify(get_total_cost_of_an_order(order_id))

@app.route('/api/orders_between_dates')
def orders_between_dates():
    after = request.args.get('after')
    before = request.args.get('before')
    print("LOLOLOL", after, before)
    return jsonify(get_orders_between_dates(after, before))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
