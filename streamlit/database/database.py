
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from Config.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(
    connection_url,
    pool_pre_ping=True
)


def test_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True


def get_data(query, params=None):
    with engine.connect() as connection:
        return pd.read_sql(
            text(query),
            connection,
            params=params or {}
        )
