import os
import asyncio
from flask import Flask, jsonify, request

from db_accessor import (
    get_customers,
    get_orders_of_customer,
    get_total_cost_of_an_order,
    get_orders_between_dates,
    insert_order_items,
)
from formatters import str_to_date

app = Flask(__name__)


@app.route("/")
async def hello():
    return "<h1>Welcome to MarketPlace!</h1>"


@app.route("/api/customers")
async def customers():
    customers = get_customers()
    return jsonify([c async for c in customers])


@app.route("/api/orders")
async def orders():
    cust_id = int(request.args.get("cust_id"))
    orders = await get_orders_of_customer(cust_id)
    return jsonify(orders)


@app.route("/api/order_total")
async def order_total():
    order_id = int(request.args.get("order_id"))
    total = await get_total_cost_of_an_order(order_id)
    return jsonify(total)


@app.route("/api/orders_total")
async def orders_total():
    orders = request.json.get("orders", [])
    async with asyncio.TaskGroup() as tg:
        order_tasks = [
            tg.create_task(get_total_cost_of_an_order(order)) for order in orders
        ]
    return jsonify([task.result() for task in order_tasks])


@app.route("/api/orders_between_dates")
async def orders_between_dates():
    after = str_to_date(request.args.get("after"))
    before = str_to_date(request.args.get("before"))

    orders = get_orders_between_dates(after, before)

    return jsonify([order async for order in orders])


@app.route("/api/add_order_items", methods=["POST"])
async def add_order_items():
    order_id = request.json.get("order_id")
    item_id = request.json.get("item_id")
    quantity = request.json.get("quantity")
    item = await insert_order_items(order_id, item_id, quantity)
    return jsonify(item)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
