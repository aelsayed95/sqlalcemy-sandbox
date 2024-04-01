from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy import select, ForeignKey, UniqueConstraint
from db.base import Base, engine
from db.address import Address
from typing import Any

class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"))

    address: Mapped["Address"] = relationship(lazy="joined") # one to one

    __table_args__ = (UniqueConstraint("address_id"),)


    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, address_id={self.address_id!r}, address={self.address})"

    @classmethod
    def get_customers(cls) -> list["Customer"]:
        with Session(engine) as session:
            stmt = select(Customer)
            result = session.execute(stmt)
            customers = result.scalars().all()

            return customers

    @classmethod
    def as_dict(cls, customers):
    
        return [{c.name: getattr(customer, c.name)
                 for c in customer.__table__.columns} | 
                 {c.name: getattr(customer.address, c.name) 
                  for c in customer.address.__table__.columns} 
                 for customer in customers]