from db.base import engine
from db.customer import Customer
from db.item import Item
from db.order_items import OrderItems
from db.orders import Orders
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def get_customers():
    with Session(engine) as session:
        stmt = select(Customer)
        result = session.execute(stmt)
        customers = result.scalars().all()

    return [customer.as_dict() for customer in customers]


def get_orders_of_customer(customer_id):
    with Session(engine) as session:
        result = session.execute(
            select(Orders).where(Orders.customer_id == customer_id)
        )
        orders = result.scalars().unique().all()

    return [order.as_dict() for order in orders]


def get_total_cost_of_an_order(order_id):
    with Session(engine) as session:
        result = session.execute(
            select(func.sum(Item.price * OrderItems.quantity).label("total_cost"))
            .join(Orders.order_items)
            .join(OrderItems.item)
            .where(Orders.id == order_id)
        )
        total_cost = result.scalars().one()
        return {"total_cost": total_cost}


def get_orders_between_dates(after, before):
    with Session(engine) as session:
        result = session.execute(
            select(Orders).where(Orders.order_time.between(after, before))
        )
        orders = result.scalars().unique().all()

    return [order.as_dict() for order in orders]


def insert_order_items(order_id, item_id, quantity):
    new_order_item = OrderItems(order_id=order_id, item_id=item_id, quantity=quantity)
    with Session(engine) as session:
        session.add(new_order_item)
        session.commit()
