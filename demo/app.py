from starlette.applications import Starlette
from starlette.routing import Route

from .cases import HomePage, MapPage, Ping, SharePage
from .handlers import PageHandler, ShareHandler
from .repos import FrequencyRepo


class Container:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class App:
    def __init__(self):
        self._repos = Container(frequencies=FrequencyRepo())
        self._cases = Container(
            home=HomePage(),
            map=MapPage(self._repos.frequencies),
            share=SharePage(self._repos.frequencies),
            ping=Ping(),
        )
        self._handlers = Container(
            home=PageHandler(self._cases.home),
            map=PageHandler(self._cases.map),
            share=ShareHandler(self._cases.share),
            ping=PageHandler(self._cases.ping),
        )

        h = self._handlers
        self._routes = [
            Route("/", endpoint=h.home.__call__),
            Route("/map", endpoint=h.map.__call__),
            Route("/share", endpoint=h.share.__call__, methods=["GET", "POST"]),
            Route("/ping", endpoint=h.ping.__call__),
        ]

    def app(self):
        return Starlette(debug=True, routes=self._routes)
