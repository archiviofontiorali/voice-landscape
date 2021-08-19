import sqlite3

from .models import Path

# from loguru import logger


class SQLite:
    def __init__(self, db_path: Path):
        self._db_path = str(db_path)

    def execute(self, query: str, **kwargs):
        with sqlite3.connect(self._db_path) as connection:
            return connection.execute(query, kwargs)

    def create_table(self, table: str, keys: str):
        self.execute(f"CREATE TABLE IF NOT EXISTS {table} ({keys})")
