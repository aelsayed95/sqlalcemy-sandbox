from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy import select, ForeignKey
from db.base import Base, engine
from db.address import Address
from typing import Any

class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"))

    address: Mapped["Address"] = relationship(lazy="joined")

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, address_id={self.address_id!r}, address={self.address})"

    @classmethod
    def get_customers(cls) -> list[dict[str, Any]]:
        with Session(engine) as session:
            stmt = select(Customer)
            result = session.execute(stmt)
            customers = result.scalars().all()

        return [{"id": customer.id,
                "name": customer.name,
                "flat_number": customer.address.flat_number,
                "post_code": customer.address.post_code}
                for customer in customers]
