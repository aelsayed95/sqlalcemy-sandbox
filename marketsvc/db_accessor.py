from db.customer import Customer

def get_customers():
    customers = Customer.get_customers()
    return customers

