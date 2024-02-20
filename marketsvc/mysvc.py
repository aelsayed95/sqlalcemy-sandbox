import os
import random
import time

from sqlalchemy import create_engine, text

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "marketdb"

db_connection_string = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(db_connection_string)
print(f"{engine=}")


def get_users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM customer"))
        print(f"Customers: {result.all()}")


if __name__ == "__main__":
    get_users()
