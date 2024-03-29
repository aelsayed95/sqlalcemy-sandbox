from sqlalchemy import text
from db.base import engine

def execute_query(query, params=None, insert=False):
    with engine.connect() as conn:
        result = conn.execute(text(query), params)

        if insert:
            conn.commit()
            return

        return [row._asdict() for row in result]


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
            item.price*order_items.quantity AS total
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.customer_id=:customer_id
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
            SUM(item.price*order_items.quantity) AS total
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.id=:order_id
        """,
        {"order_id": order_id},
    )

    for row in rows:
        print(row)

    return rows[0]


def get_orders_between_dates(after, before):
    rows = execute_query(
        f"""
        SELECT
            customer.name,
            item.name, 
            item.price, 
            item.price*order_items.quantity AS total
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
            orders.order_time >= :after
        AND
            orders.order_time <= :before
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
                (:order_id, :item_id, :quantity)
            """,
            {"order_id": order_id, "item_id": item_id, "quantity": quantity},
            insert=True,
        )

        return "200 OK"

    except:
        return "500 Error"
