from sqlalchemy import text
from db.base import create_engine

import logging


async def execute_insert_query(query, params):
    async with create_engine().begin() as conn:
        result = await conn.execute(text(query), params)
        await conn.commit()
    return []


async def execute_query(query, params=None, insert=False):
    async with create_engine().begin() as conn:
        result = await conn.execute(text(query), params)
        return [row._asdict() for row in result]


async def stream_query(query, params=None, insert=False):
    async with create_engine().begin() as conn:
        # https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/basic.html
        # for a streaming result that buffers only segments of the
        # result at time, the AsyncConnection.stream() method is used.
        # this returns a sqlalchemy.ext.asyncio.AsyncResult object.
        result = await conn.stream(text(query), params)
        async for row in result:
            yield row._asdict()


def get_customers():
    rows = stream_query("SELECT * FROM customer")
    return rows


async def get_orders_of_customer(customer_id):
    rows = await execute_query(
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
    return rows


async def get_total_cost_of_an_order(order_id):
    rows = await execute_query(
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
    return rows[0]


def get_orders_between_dates(after, before):
    rows = stream_query(
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
    return rows


async def insert_order_items(order_id, item_id, quantity):
    try:
        await execute_insert_query(
            f"""
            INSERT INTO order_items
            VALUES
                (:order_id, :item_id, :quantity)
            """,
            {"order_id": order_id, "item_id": item_id, "quantity": quantity},
        )

        return "200 OK"

    except Exception:
        logging.exception("Failed to add order items")
        return "500 Error"
