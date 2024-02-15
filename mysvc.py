#!/usr/local/bin/python3.11

# code from: 
# https://stefanopassador.medium.com/docker-compose-with-python-and-posgresql-45c4c5174299

import time
import random
import os

from sqlalchemy import create_engine

db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_port = os.environ.get('POSTGRES_PORT')
db_host = 'mydb'

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

def add_new_row(n):
    # Insert a new number into the 'numbers' table.
    stmt = f"INSERT INTO numbers (number,timestamp) VALUES "
    f"({n}, {int(round(time.time() * 1000))});"
    db.execute(stmt)

def get_last_row():
    # Retrieve the last number inserted inside the 'numbers'
    query = "" + \
            "SELECT number " + \
            "FROM numbers " + \
            "WHERE timestamp >= (SELECT max(timestamp) FROM numbers)" +\
            "LIMIT 1"

    result_set = db.execute(query)  
    for (r) in result_set:  
        return r[0]

if __name__ == '__main__':
    print('Application started')
    
    while True:
        add_new_row(random.randint(1,100000))
        print('The last value insterted is: {}'.format(get_last_row()))
        time.sleep(5)
