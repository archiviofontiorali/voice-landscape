from starlette.applications import Starlette
from starlette.routing import Route

from .cases import FoliumMapPage, HomePage, LeafletMapPage, Ping, SharePage
from .handlers import PageHandler, ShareHandler
from .repos import FoliumMapRepo, FrequencyDictRepo
from .system.structures import Container


class App:
    def __init__(self):
        self._services = Container()

        s = self._services
        self._repos = Container(
            frequencies=FrequencyDictRepo(),
            map=FoliumMapRepo(),
        )

        r = self._repos
        self._cases = Container(
            home=HomePage(),
            map=LeafletMapPage(r.frequencies),
            legacy_map=FoliumMapPage(r.frequencies, r.map),
            share=SharePage(r.frequencies),
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
        ]

    def app(self):
        return Starlette(debug=True, routes=self._routes)
