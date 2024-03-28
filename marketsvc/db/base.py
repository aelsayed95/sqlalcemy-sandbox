import os
from typing import Optional, List
from sqlalchemy import String
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "marketdb"

url_object = URL.create(
    "postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
    port=DB_PORT
)

engine = create_engine(url_object, echo=True)

class Base(DeclarativeBase):
    pass

class Item(Base):
     __tablename__ = "item"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(120))
     price: Mapped[int] = mapped_column()
     description: Mapped[Optional[str]] = mapped_column()

     def __repr__(self) -> str:
         return f"Item(id={self.id!r}, name={self.name!r}, price={self.price!r}), description={self.description!r})"
