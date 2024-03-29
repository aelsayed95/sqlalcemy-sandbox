from db.customer import Customer
from db.orders import Orders

def get_customers():
    customers = Customer.get_customers()
    return customers

def get_orders_of_customer(customer_id):
    orders = Orders.get_orders_by_customer_id(customer_id)
    return orders