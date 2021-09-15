import sqlite3

import databases

from . import config
from .models import Path


class Database:
    def __init__(self):
        self._db = databases.Database(config.DATABASE_URL)

    async def connect(self):
        await self._db.connect()

    async def disconnect(self):
        await self._db.disconnect()

    async def execute(self, query: str, **values) -> int:
        return await self._db.execute(query=query, values=values)

    async def fetch_all(self, query: str, **values):
        return await self._db.fetch_all(query=query, values=values)

    async def create_table(self, table: str, keys: str):
        await self.execute(f"CREATE TABLE IF NOT EXISTS {table} ({keys})")


class SQLite:
    def __init__(self, db_path: Path):
        self._db_path = str(db_path)

    def execute(self, query: str, **kwargs):
        with sqlite3.connect(self._db_path) as connection:
            return connection.execute(query, kwargs)

    def create_table(self, table: str, keys: str):
        self.execute(f"CREATE TABLE IF NOT EXISTS {table} ({keys})")
