from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy import ForeignKey
from db.base import Base, engine
from db.item import Item
from typing import Any
from datetime import datetime

class OrderItems(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    quantity: Mapped[int]

    orders: Mapped[list["Orders"]] = relationship(lazy="joined")
    item: Mapped["Item"] = relationship(lazy="joined")

    def __repr__(self) -> str:
        return f"OrderItems(order_id={self.order_id!r}, item_id={self.item_id!r}, quantity={self.quantity!r}, orders={self.orders}, item={self.item})"

