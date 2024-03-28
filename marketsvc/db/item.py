from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, engine


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str | None]

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, price={self.price!r}, description={self.description!r})"
