from db.customer import Customer

def _orms_to_dict(orms):
    return [{key: val for key, val in orm.__dict__.items() if key != "_sa_instance_state"} for orm in orms]

def get_customers():
    customers = Customer.get_customers()
    return _orms_to_dict(customers)

