from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from . import services
from .cases import HomePage, LeafletMapPage, Ping, SharePage, ShowcasePage, SpeechToText
from .config import DEBUG
from .handlers import PageHandler, ShareHandler, STTHandler
from .repos import FrequencySQLRepo
from .system.structures import Container


class App:
    def __init__(self):
        self._services = Container(db=services.Database())

        s = self._services
        self._repos = Container(frequencies=FrequencySQLRepo(s.db))

        r = self._repos
        self._cases = Container(
            home=HomePage(),
            map=LeafletMapPage(r.frequencies),
            showcase=ShowcasePage(r.frequencies),
            share=SharePage(r.frequencies),
            stt=SpeechToText(),
            ping=Ping(),
        )

        c = self._cases
        self._handlers = Container(
            home=PageHandler(c.home),
            map=PageHandler(c.map),
            showcase=PageHandler(c.showcase),
            share=ShareHandler(c.share),
            stt=STTHandler(c.stt),
            ping=PageHandler(c.ping),
        )

        h = self._handlers
        self._routes = [
            Route("/", endpoint=h.home.__call__),
            Route("/map", endpoint=h.map.__call__),
            Route("/showcase", endpoint=h.showcase.__call__),
            Route("/share", endpoint=h.share.__call__, methods=["GET", "POST"]),
            Route("/api/stt", endpoint=h.stt.__call__, methods=["POST"]),
            Route("/ping", endpoint=h.ping.__call__),
            Mount("/", app=StaticFiles(directory="www"), name="static"),
        ]

    def app(self):
        return Starlette(
            debug=DEBUG,
            routes=self._routes,
            on_startup=[self._services.db.connect, self._repos.frequencies.init_db],
            on_shutdown=[self._services.db.disconnect],
        )
