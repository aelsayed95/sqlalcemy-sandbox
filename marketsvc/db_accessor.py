import os
import psycopg2
from sqlalchemy import text, URL
from db.base import engine

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "marketdb"

def execute_query(query, params=None, insert=False):
    with engine.connect() as conn:
        result = conn.execute(text(query), params)

        if insert:
            conn.commit()
            return

        return [row._asdict() for row in result.all()]


def get_customers():
    rows = execute_query("SELECT * FROM customer")
    for row in rows:
        print(row)
    return rows


def get_orders_of_customer(customer_id):
    rows = execute_query(
        f"""
        SELECT 
            item.name, 
            item.description, 
            item.price, 
            item.price*order_items.quantity
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.customer_id=%(customer_id)s
        """,
        {"customer_id": customer_id},
    )
    for row in rows:
        print(row)
    return rows


def get_total_cost_of_an_order(order_id):
    rows = execute_query(
        f"""
        SELECT 
            SUM(item.price*order_items.quantity)
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.id=%(order_id)s
        """,
        {"order_id": order_id},
    )

    for row in rows:
        print(row)

    return {"Order Total": rows[0][0]}


def get_orders_between_dates(after, before):
    rows = execute_query(
        f"""
        SELECT
            customer.name,
            item.name, 
            item.price, 
            item.price*order_items.quantity
        FROM orders 
        JOIN customer
        ON
            customer.id = orders.customer_id
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.order_time >= %(after)s
        AND
            orders.order_time <= %(before)s
        """,
        {"after": after, "before": before},
    )
    for row in rows:
        print(row)
    return rows


def insert_order_items(order_id, item_id, quantity):
    try:
        execute_query(
            f"""
            INSERT INTO order_items
            VALUES
                (%(order_id)s, %(item_id)s, %(quantity)s)
            """,
            {"order_id": order_id, "item_id": item_id, "quantity": quantity},
            insert=True,
        )

        return "200 OK"

    except:
        return "500 Error"


if __name__ == "__main__":
    # get_customers()
    get_orders_of_customer(1)
