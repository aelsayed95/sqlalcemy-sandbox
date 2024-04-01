from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy import select, ForeignKey
from sqlalchemy.sql import func
from db.base import Base, engine
from db.customer import Customer
from db.order_items import OrderItems
from db.item import Item
from datetime import datetime

class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    order_time: Mapped[datetime]

    customer: Mapped["Customer"] = relationship(lazy="joined") # many to one
    order_items: Mapped[list["OrderItems"]] = relationship(lazy="joined") # one to many

    def __repr__(self) -> str:
        return f"Orders(id={self.id!r}, customer_id={self.customer_id!r}, order_time={self.order_time!r}, customer={self.customer})"


    @classmethod
    def get_orders_by_customer_id(cls, customer_id):
        with Session(engine) as session:
            stmt = select(Orders).where(Orders.customer_id == customer_id)
            result = session.execute(stmt)
            orders = result.scalars().unique().all()

            return [{"name": order_item.item.name,
                    "description": order_item.item.description,
                    "price": order_item.item.price,
                    "total": order_item.item.price * order_item.quantity,}
                    for order in orders 
                    for order_item in order.order_items]

    @classmethod
    def get_total_cost_of_an_order(cls, order_id):
        with Session(engine) as session:
            result = session.execute(select(func.sum(Item.price * OrderItems.quantity)
                                            .label("total_cost"))
                                     .join(Orders.order_items)
                                     .join(OrderItems.item)
                                     .where(Orders.id == order_id))
            total_cost = result.scalars().all()
            return total_cost