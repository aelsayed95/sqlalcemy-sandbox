from sqlalchemy.orm import Session
from db.base import engine
from db.customer import Customer
from db.orders import Orders
from db.order_items import OrderItems

def get_customers():
    customers = Customer.get_customers()
    return Customer.as_dict(customers)

def get_orders_of_customer(customer_id):
    orders = Orders.get_orders_by_customer_id(customer_id)
    return orders

def get_total_cost_of_an_order(order_id):
    total_cost = Orders.get_total_cost_of_an_order(order_id)
    return total_cost

def get_orders_between_dates(after, before):
    orders = Orders.get_orders_between_dates(after, before)
    return orders

def insert_order_items(order_id, item_id, quantity):
    new_order_item = OrderItems(order_id=order_id, item_id=item_id, quantity=quantity)
    with Session(engine) as session:
        session.add(new_order_item)
        session.commit()