import spacy
from loguru import logger
from starlette.responses import PlainTextResponse
from starlette.templating import Jinja2Templates

from .geo import Coordinates
from .repos import FoliumMapRepo, FrequencyRepo

# TODO: create presenters
templates = Jinja2Templates(directory="demo/templates")


class HomePage:
    @staticmethod
    async def execute(request):
        context = {"request": request}
        return templates.TemplateResponse("index.html", context)


class MapPage:
    def __init__(self, frequency_repo: FrequencyRepo, map_repo: FoliumMapRepo):
        self._frequency_repo = frequency_repo
        self._map_repo = map_repo

    async def execute(self, request):
        _map = self._map_repo.generate_map(self._frequency_repo)
        context = {
            "map": _map,
            "request": request,
        }
        return templates.TemplateResponse("map.html", context)


class SharePage:
    def __init__(self, frequencies: FrequencyRepo):
        self._frequencies = frequencies
        self._nlp = spacy.load("it_core_news_sm")

    async def execute(self, target: Coordinates, text: str, request):
        if request.method == "POST":
            logger.debug(f"Receiving text from {target}: {text}")
            nearest_place = self._frequencies.find_nearest_place(target)

            doc = self._nlp(text)
            for token in doc:
                if token.tag_ in ("V", "S"):
                    self._frequencies.update_frequency(nearest_place, token.lemma_)

        context = {"request": request}
        return templates.TemplateResponse("share.html", context)


class Ping:
    def __init__(self):
        self._response = "Pong!"

    async def execute(self, request):
        logger.debug(self._response)
        return PlainTextResponse(self._response)
