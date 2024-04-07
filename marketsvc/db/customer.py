from __future__ import annotations

from db.address import Address
from db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"))

    address: Mapped["Address"] = relationship(
        back_populates="customer", lazy="joined"
    )  # one to one

    flat_number: AssociationProxy[int] = association_proxy("address", "flat_number")
    post_code: AssociationProxy[int] = association_proxy("address", "post_code")

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, name={self.name!r}, address_id={self.address_id!r}, address={self.address})"

    def as_dict(self):
        return {
            "name": self.name,
            "address": {
                "flat_number": self.flat_number,
                "post_code": self.post_code,
            },
        }
