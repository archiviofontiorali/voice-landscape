from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from . import cases, presenters, services
from .config import DEBUG
from .handlers import APIHandler, PageHandler
from .repos import FrequencySQLRepo
from .system.structures import Container
from .system.web import get, post


class App:
    def __init__(self):
        s = self._services = Container(db=services.Database())
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
            Mount("/", app=StaticFiles(directory="www"), name="static"),
        ]

    def app(self):
        return Starlette(
            debug=DEBUG,
            routes=self._routes,
            on_startup=[self._services.db.connect, self._repos.frequencies.init_db],
            on_shutdown=[self._services.db.disconnect],
        )
