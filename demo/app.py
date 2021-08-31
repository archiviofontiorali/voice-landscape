from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from .cases import HomePage, LeafletMapPage, Ping, SharePage, SpeechToText
from .handlers import PageHandler, ShareHandler, STTHandler
from .repos import FrequencySQLRepo
from .services import SQLite
from .system.structures import Container


class App:
    def __init__(self):
        self._services = Container(sqlite=SQLite("db/db.sqlite"))

        s = self._services
        self._repos = Container(
            frequencies=FrequencySQLRepo(s.sqlite),
        )

        r = self._repos
        self._cases = Container(
            home=HomePage(),
            map=LeafletMapPage(r.frequencies),
            share=SharePage(r.frequencies),
            stt=SpeechToText(),
            ping=Ping(),
        )

        c = self._cases
        self._handlers = Container(
            home=PageHandler(c.home),
            map=PageHandler(c.map),
            share=ShareHandler(c.share),
            stt=STTHandler(c.stt),
            ping=PageHandler(c.ping),
        )

        h = self._handlers
        self._routes = [
            Route("/", endpoint=h.home.__call__),
            Route("/map", endpoint=h.map.__call__),
            Route("/share", endpoint=h.share.__call__, methods=["GET", "POST"]),
            Route("/api/stt", endpoint=h.stt.__call__, methods=["POST"]),
            Route("/ping", endpoint=h.ping.__call__),
            Mount("/", app=StaticFiles(directory="www"), name="static"),
        ]

    def app(self):
        return Starlette(debug=True, routes=self._routes)
