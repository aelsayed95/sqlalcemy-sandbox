from datetime import datetime
import logging

from db.base import async_session_maker
from db.customer import Customer
from db.item import Item
from db.order_items import OrderItems
from db.orders import Orders
from sqlalchemy import select
from sqlalchemy.sql import func


async def get_customers():
    async_session = async_session_maker()
    async with async_session() as session:
        stmt = select(Customer)
        result = await session.stream(stmt)
        async for customer in result.scalars():
            yield customer.as_dict()


async def get_orders_of_customer(customer_id):
    async_session = async_session_maker()
    async with async_session() as session:
        result = await session.execute(
            select(Orders).where(Orders.customer_id == customer_id)
        )
        orders = result.scalars().unique().all()

    return [order.as_dict() for order in orders]


async def get_total_cost_of_an_order(order_id):
    async_session = async_session_maker()
    async with async_session() as session:
        result = await session.execute(
            select(func.sum(Item.price * OrderItems.quantity).label("total_cost"))
            .join(Orders.order_items)
            .join(OrderItems.item)
            .where(Orders.id == order_id)
        )
        total_cost = result.scalar()
        return {"total_cost": total_cost}


async def get_orders_between_dates(after, before):
    async_session = async_session_maker()
    async with async_session() as session:
        result = await session.stream(
            select(Orders).where(Orders.order_time.between(after, before))
        )
        async for order in result.scalars().unique():
            yield order.as_dict()


async def insert_order_items(order_id, item_id, quantity):
    try:
        async_session = async_session_maker()
        async with async_session() as session:
            new_order_item = OrderItems(
                order_id=order_id, item_id=item_id, quantity=quantity
            )
            session.add(new_order_item)
            await session.commit()

        return True
    except Exception:
        logging.exception("Failed to add items to order")
        return False


async def add_new_order_for_customer(customer_id, items):
    try:
        async_session = async_session_maker()
        async with async_session() as session:
            result = await session.execute(select(Customer).where(customer_id == customer_id))
            customer = result.scalar()

            new_order = Orders(
                customer_id=customer_id,
                order_time=datetime.now(),
                customer=customer,
            )

            session.add(new_order)
            await session.flush()

            new_order_items = [
                OrderItems(
                    order_id=new_order.id,
                    item_id=item["id"],
                    quantity=item["quantity"],
                )
                for item in items
            ]

            session.add_all(new_order_items)
            await session.commit()
        return True

    except Exception:
        logging.exception("Failed to add new order")
        return False
