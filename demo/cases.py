import spacy
from loguru import logger
from starlette.responses import PlainTextResponse
from starlette.templating import Jinja2Templates

from .constants import AFOR_COORDINATES, MAP_PROVIDER_ATTRIBUTION, MAP_PROVIDER_URL
from .geo import Coordinates, prepare_marker, find_nearest_place
from .repos import FoliumMapRepo, FrequencyDictRepo
from .models import MapOptions

# TODO: create presenters
templates = Jinja2Templates(directory="demo/templates")


class HomePage:
    @staticmethod
    async def execute(request):
        context = {"request": request}
        return templates.TemplateResponse("index.html", context)


class FoliumMapPage:
    def __init__(self, frequency_repo: FrequencyDictRepo, map_repo: FoliumMapRepo):
        self._frequency_repo = frequency_repo
        self._map_repo = map_repo

    async def execute(self, request):
        self._map_repo.update_map(self._frequency_repo)
        context = {
            "map": self._map_repo.map,
            "request": request,
        }
        return templates.TemplateResponse("legacy_map.html", context)


class LeafletMapPage:
    def __init__(self, frequency_repo: FrequencyDictRepo):
        self._frequency_repo = frequency_repo
        self._map_config = MapOptions(
            center=list(AFOR_COORDINATES),
            provider_url=MAP_PROVIDER_URL,
            provider_attribution=MAP_PROVIDER_ATTRIBUTION,
        )

    async def execute(self, request):
        markers = [
            prepare_marker(place, self._frequency_repo)
            for place in self._frequency_repo.places
        ]
        context = {
            "map_config": self._map_config,
            "markers": markers,
            "request": request,
        }
        return templates.TemplateResponse("map.html", context)


class SharePage:
    def __init__(self, frequency_repo: FrequencyDictRepo):
        self._frequency_repo = frequency_repo
        self._nlp = spacy.load("it_core_news_sm")

    async def execute(self, target: Coordinates, text: str, request):
        if request.method == "POST":
            logger.debug(f"Receiving text from {target}: {text}")
            nearest_place, _ = find_nearest_place(target, self._frequency_repo.places)

            doc = self._nlp(text)
            for token in doc:
                if token.tag_ in ("V", "S"):
                    self._frequency_repo.update_frequency(nearest_place, token.lemma_)

        context = {"request": request}
        return templates.TemplateResponse("share.html", context)


class Ping:
    def __init__(self):
        self._response = "Pong!"

    async def execute(self, request):
        logger.debug(self._response)
        return PlainTextResponse(self._response)
