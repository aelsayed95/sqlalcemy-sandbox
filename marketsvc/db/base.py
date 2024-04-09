import os

from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "marketdb"

url_object = URL.create(
    "postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
    port=DB_PORT,
)


def create_engine():
    return create_async_engine(url_object, echo=True)
