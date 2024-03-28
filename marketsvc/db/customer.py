from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import select
from db.base import Base, engine


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address_id: Mapped[int]

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, address_id={self.address_id!r})"

    @classmethod
    def get_customers(cls) -> list["Customer"]:
        with Session(engine) as session:
            stmt = select(Customer)
            result = session.execute(stmt)
            customers = result.scalars().all()

        return customers