import contextlib

import databases
from starlette.applications import Starlette

from . import cases, constants, presenters
from .handlers import APIHandler, PageHandler
from .repos import FrequencySQLRepo
from .system.structures import Container
from .system.web import get, post


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
            text=presenters.Text(),
        )
        c = self._cases = Container(
            home=cases.TemplatePage("index.html"),
            map=cases.LeafletMapPage("map.html", r.frequencies),
            showcase=cases.ShowcasePage("showcase.html", r.frequencies),
            share=cases.SharePage("share.html", r.frequencies),
            stt=cases.SpeechToText(),
            privacy=cases.TemplatePage("privacy.html"),
            ping=cases.Ping(),
        )
        h = self._handlers = Container(
            home=PageHandler(c.home, p.template),
            map=PageHandler(c.map, p.template),
            showcase=PageHandler(c.showcase, p.template),
            share=PageHandler(c.share, p.template),
            stt=APIHandler(c.stt, p.json),
            privacy=PageHandler(c.privacy, p.template),
            ping=PageHandler(c.ping, p.text),
        )
        self._routes = [
            get("/", h.home),
            get("/map", endpoint=h.map),
            get("/showcase", endpoint=h.showcase),
            get("/share", endpoint=h.share),
            post("/share", endpoint=h.share),
            get("/privacy", endpoint=h.privacy),
            post("/api/stt", endpoint=h.stt),
            get("/ping", endpoint=h.ping),
        ]

    def app(self):
        return Starlette(
            debug=constants.DEBUG,
            routes=self._routes,
            on_startup=[self._services.db.connect, self._repos.frequencies.init_db],
            on_shutdown=[self._services.db.disconnect],
        )
