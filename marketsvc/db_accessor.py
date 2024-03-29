from db.customer import Customer
from db.orders import Orders

def get_customers():
    customers = Customer.get_customers()
    return Customer.as_dict(customers)

def get_orders_of_customer(customer_id):
    orders = Orders.get_orders_by_customer_id(customer_id)
    return orders

def get_total_cost_of_an_order(order_id):
    total_cost = Orders.get_total_cost_of_an_order(order_id)
    return total_cost