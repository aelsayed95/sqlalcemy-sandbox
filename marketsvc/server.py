import os
from flask import Flask, jsonify, request

from db_accessor import get_customers, get_orders_of_customer

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
