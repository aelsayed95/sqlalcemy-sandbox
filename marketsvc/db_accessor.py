import os

import psycopg2

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "marketdb"


def execute_query(query, params=None):
    with psycopg2.connect(
        database=DB_HOST, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT
    ) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return rows


def execute_insert_query(query):
    with psycopg2.connect(
        database=DB_HOST, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT
    ) as conn:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()


def get_customers():
    rows = execute_query("SELECT * FROM customer")
    return rows


def get_orders_of_customer(customer_id):
    rows = execute_query(
        """
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
    return rows


def get_total_cost_of_an_order(order_id):
    rows = execute_query(
        """
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
        """
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
        execute_insert_query(
            """
            INSERT INTO order_items
            VALUES
                (%(order_id)s, %(item_id)s, %(quantity)s)
            """,
            {"order_id": order_id, "item_id": item_id, "quantity": quantity},
        )

        return "200 OK"

    except Exception:
        return False
