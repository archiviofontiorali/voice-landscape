import math
from abc import ABC, abstractmethod
from typing import Any, Iterable, Literal, Tuple

import geopy.distance
import numpy as np
import spacy
import spacy.symbols
from loguru import logger
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route
from starlette.templating import Jinja2Templates

Coordinates = tuple[float, float]

PLACES = {
    (44.65461615128406, 10.901229167243947): "AFOr | Archivio fonti orali",
}

# a = np.array([44.647728027899625, 10.88466746283678])
# b = np.array([44.64159324683118, 10.902033051497972])
# c = np.array([44.65583248401956, 10.903694945558476])
# v1, v2 = b - a, c - a
#
# N = 6
# points = np.empty(((N + 1) * (N + 2) // 2, 2))
# count = 0
# for i in range(N + 1):
#     for j in range(N - i + 1):
#         points[count, :] = a + (i / N) * v1 + (j / N) * v2
#         count += 1
#
#
# for i, p in enumerate(points):
#     PLACES[(p[0], p[1])] = f"place #{i}"


# Structures


class Container(dict):
    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(f"'Container' object has no attribute '{item}'")


# Presenters


class Template:
    def __init__(self, directory: str = "templates"):
        self.templates = Jinja2Templates(directory=directory)

    def render(self, template: str, context: dict):
        return self.templates.TemplateResponse(template, context)


# Repos


class FrequencySQLRepo:
    places: Iterable[Coordinates]

    def __init__(self, db):
        self._db = db
        self._table = "frequencies"
        self._keys = ", ".join(
            [
                "latitude FLOAT8 NOT NULL",
                "longitude FLOAT8 NOT NULL",
                "word TEXT NOT NULL",
                "frequency INT DEFAULT 1",
                "PRIMARY KEY(latitude, longitude, word)",
            ]
        )

        self._coordinates = list(PLACES.keys())

    @property
    def places(self) -> Iterable[Coordinates]:
        return self._coordinates

    async def update_frequency(self, place: Coordinates, key: str):
        values = dict(latitude=place[0], longitude=place[1], word=key)
        query = (
            f"INSERT INTO {self._table}(latitude, longitude, word) "
            "VALUES (:latitude, :longitude, :word) "
            "ON CONFLICT (latitude, longitude, word) "
            "DO UPDATE SET frequency = frequencies.frequency + 1"
        )
        await self._db.execute(query, **values)


# Cases


class Case(ABC):
    @abstractmethod
    async def execute(self, request: Request, presenter) -> dict:
        pass


class SharePage(Case):
    VALID_TOKENS = (
        spacy.symbols.ADV,
        spacy.symbols.NOUN,
        spacy.symbols.VERB,
        spacy.symbols.ADJ,
    )

    def __init__(self, template: str, frequency_repo: FrequencySQLRepo):
        self.template = template
        self._frequency_repo = frequency_repo
        self._nlp = spacy.load("it_core_news_sm")

    @staticmethod
    def find_nearest_place(
        target: Coordinates, places: Iterable[Coordinates]
    ) -> Tuple[Coordinates, float]:
        near, distance = None, math.inf
        for place in places:
            new_distance = geopy.distance.geodesic(target, place).m
            if new_distance < distance:
                near, distance = place, new_distance
        return near, distance

    async def execute(self, request, presenter):
        if request.method == "POST":
            data = await request.form()

            coordinates = (
                float(data.get("loc-x", None)),
                float(data.get("loc-y", None)),
            )
            text = data.get("text", None)

            logger.debug(f"Receiving text from {coordinates}: {text}")
            nearest, _ = self.find_nearest_place(
                coordinates, self._frequency_repo.places
            )

            for token in self._nlp(text):
                if token.pos not in self.VALID_TOKENS:
                    continue
                await self._frequency_repo.update_frequency(nearest, token.lemma_)

        context = {"request": request}
        return presenter.render(self.template, context)


# Handler


class Handler(ABC):
    case: Case
    presenter: Any

    def __init__(self, case: Case, presenter):
        self.case = case
        self.presenter = presenter

    @abstractmethod
    async def __call__(self, request: Request):
        pass


templates = Jinja2Templates(directory="templates")


class PageHandler(Handler):
    async def __call__(self, request):
        return await self.case.execute(request, self.presenter)


# Routing

Method = Literal["GET", "POST"]


def route(path: str, endpoint: Handler, method: Method = "GET", **kwargs) -> Route:
    endpoint = getattr(endpoint, method.lower(), endpoint.__call__)
    return Route(path, endpoint=endpoint, methods=[method], **kwargs)


def get(path: str, endpoint: Handler, **kwargs):
    return route(path, endpoint, "GET", **kwargs)


def post(path: str, endpoint: Handler, **kwargs):
    return route(path, endpoint, "POST", **kwargs)


# App


class App:
    def __init__(self):
        r = self._repos = Container(frequencies=FrequencySQLRepo(db=None))
        p = self._presenters = Container(template=Template())
        c = self._cases = Container(
            share=SharePage("share.html", r.frequencies),
        )
        h = self._handlers = Container(
            share=PageHandler(c.share, p.template),
        )
        self._routes = [
            get("/share", endpoint=h.share),
            post("/share", endpoint=h.share),
        ]

    def app(self):
        return Starlette(debug=True, routes=self._routes)
