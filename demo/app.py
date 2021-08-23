from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from .cases import FoliumMapPage, HomePage, LeafletMapPage, Ping, SharePage
from .handlers import PageHandler, ShareHandler
from .repos import FoliumMapRepo, FrequencyDictRepo, FrequencySQLRepo
from .services import SQLite
from .system.structures import Container


class App:
    def __init__(self):
        self._services = Container(sqlite=SQLite("db/db.sqlite"))

        s = self._services
        self._repos = Container(
            frequencies=FrequencyDictRepo(),
            frequencies_db=FrequencySQLRepo(s.sqlite),
            map=FoliumMapRepo(),
        )

        r = self._repos
        self._cases = Container(
            home=HomePage(),
            map=LeafletMapPage(r.frequencies_db),
            legacy_map=FoliumMapPage(r.frequencies_db, r.map),
            share=SharePage(r.frequencies_db),
            ping=Ping(),
        )

        self._handlers = Container(
            home=PageHandler(self._cases.home),
            map=PageHandler(self._cases.map),
            legacy_map=PageHandler(self._cases.legacy_map),
            share=ShareHandler(self._cases.share),
            ping=PageHandler(self._cases.ping),
        )

        h = self._handlers
        self._routes = [
            Route("/", endpoint=h.home.__call__),
            Route("/map", endpoint=h.map.__call__),
            Route("/legacy_map", endpoint=h.legacy_map.__call__),
            Route("/share", endpoint=h.share.__call__, methods=["GET", "POST"]),
            Route("/ping", endpoint=h.ping.__call__),
            Mount("/", app=StaticFiles(directory="www"), name="static"),
        ]

    def app(self):
        return Starlette(debug=True, routes=self._routes)
