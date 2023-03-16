import contextlib

import databases
from starlette.applications import Starlette

from . import cases, constants, presenters
from .handlers import APIHandler, PageHandler
from .repos import FrequencySQLRepo
from .system.web import get, post


class Container(dict):
    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(f"'Container' object has no attribute '{item}'")


class Database:
    database: databases.Database

    def __init__(self, database: databases.DatabaseURL | str):
        if isinstance(database, str):
            database = databases.DatabaseURL(database)
        self.database = databases.Database(database)

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


class App:
    def __init__(self):
        s = self._services = Container(db=Database(constants.DATABASE_URL))
        r = self._repos = Container(frequencies=FrequencySQLRepo(s.db))
        p = self._presenters = Container(
            template=presenters.Template(),
            json=presenters.JSON(),
        )
        c = self._cases = Container(
            share=cases.SharePage("share.html", r.frequencies),
            stt=cases.SpeechToText(),
        )
        h = self._handlers = Container(
            share=PageHandler(c.share, p.template),
            stt=APIHandler(c.stt, p.json),
        )
        self._routes = [
            get("/share", endpoint=h.share),
            post("/share", endpoint=h.share),
            post("/api/stt", endpoint=h.stt),
        ]

    def app(self):
        return Starlette(
            debug=constants.DEBUG,
            routes=self._routes,
            on_startup=[self._services.db.connect, self._repos.frequencies.init_db],
            on_shutdown=[self._services.db.disconnect],
        )
