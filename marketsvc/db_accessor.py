import os
import asyncpg
import logging

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "marketdb"


async def execute_query(query, *params):
    conn = await asyncpg.connect(
        database=DB_HOST,
        user=DB_USER,
        host=DB_HOST,
        password=DB_PASSWORD,
        port=DB_PORT,
    )
    async with conn.transaction():
        rows = await conn.fetch(query, *params)
        return [dict(row) for row in rows]


async def stream_query(query, *params):
    conn = await asyncpg.connect(
        database=DB_HOST,
        user=DB_USER,
        host=DB_HOST,
        password=DB_PASSWORD,
        port=DB_PORT,
    )
    async with conn.transaction():
        async for row in conn.cursor(query, *params):
            yield dict(row)


async def execute_insert_query(query, params):
    conn = await asyncpg.connect(
        database=DB_HOST,
        user=DB_USER,
        host=DB_HOST,
        password=DB_PASSWORD,
        port=DB_PORT,
    )
    async with conn.transaction():
        conn.cursor(query, params)
        conn.commit()


def get_customers():
    rows = stream_query("SELECT * FROM customer")
    return rows


async def get_orders_of_customer(customer_id):
    rows = await execute_query(
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
            orders.customer_id=$1
        """,
        customer_id,
    )
    return rows


async def get_total_cost_of_an_order(order_id):
    rows = await execute_query(
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
            orders.id=$1
        """,
        order_id,
    )
    return rows[0]["sum"]


def get_orders_between_dates(after, before):
    rows = stream_query(
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
            orders.order_time >= $1
        AND
            orders.order_time <= $2
        """,
        after,
        before,
    )
    return rows


async def insert_order_items(order_id, item_id, quantity):
    try:
        await execute_insert_query(
            """
            INSERT INTO order_items
            VALUES
                ($1, $2, $3)
            """,
            order_id,
            item_id,
            quantity,
        )
        return True

    except Exception:
        logging.exception("Failed to update order")
        return False
