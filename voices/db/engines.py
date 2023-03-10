import contextlib

import databases


class Database:
    database: databases.Database

    def __init__(self, database: databases.Database | databases.DatabaseURL | str):
        match database:
            case databases.Database():
                self.database = database
            case str() | databases.DatabaseURL():
                self.database = databases.Database(database)
            case _:
                raise AttributeError(
                    "database should be a valid DB url or a Database object"
                )

    @contextlib.asynccontextmanager
    async def lifespan(self):
        await self.database.connect()
        yield
        await self.database.disconnect()

    async def connect(self):
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()

    async def execute(self, query: str, **values) -> int:
        return await self.database.execute(query=query, values=values)

    async def fetch_all(self, query: str, **values):
        return await self.database.fetch_all(query=query, values=values)

    async def create_table(self, table: str, keys: str):
        await self.execute(f"CREATE TABLE IF NOT EXISTS {table} ({keys})")
