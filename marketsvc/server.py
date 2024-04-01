import os

from db_accessor import (
    get_customers,
    get_orders_between_dates,
    get_orders_of_customer,
    get_total_cost_of_an_order,
    insert_order_items,
    add_new_order_for_customer,
)
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Welcome to MarketPlace!</h1>"


@app.route("/api/customers")
def customers():
    return jsonify(get_customers())


@app.route("/api/orders")
def orders():
    cust_id = request.args.get("cust_id")
    return jsonify(get_orders_of_customer(cust_id))


@app.route("/api/order_total")
def order_total():
    order_id = request.args.get("order_id")
    return jsonify(get_total_cost_of_an_order(order_id))


@app.route("/api/orders_between_dates")
def orders_between_dates():
    after = request.args.get("after")
    before = request.args.get("before")
    return jsonify(get_orders_between_dates(after, before))


@app.route("/api/add_order_items", methods=["POST"])
def add_order_items():
    order_id = request.json.get("order_id")
    item_id = request.json.get("item_id")
    quantity = request.json.get("quantity")
    return jsonify(insert_order_items(order_id, item_id, quantity))


@app.route("/api/add_new_order", methods=["POST"])
def add_new_order():
    customer_id = request.json.get("customer_id")
    items = request.json.get("items")
    return jsonify(add_new_order_for_customer(customer_id, items))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
