from sqlalchemy.orm import Mapped, mapped_column

from marketsvc.db.base import Base, engine


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    flat_number: Mapped[str]
    post_code: Mapped[str]

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, flat_number={self.flat_number!r}, post_code={self.post_code!r})"
