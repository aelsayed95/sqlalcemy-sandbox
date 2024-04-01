from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base, engine

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    flat_number: Mapped[int]
    post_code: Mapped[int]

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, flat_number={self.flat_number!r}, post_code={self.post_code!r})"
