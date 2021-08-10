import folium
import spacy
from loguru import logger
from starlette.responses import PlainTextResponse
from starlette.templating import Jinja2Templates
from wordcloud import WordCloud

from .geo import Coordinates
from .repos import FrequencyRepo

# TODO: move to "constant" module
AFOR_COORDINATES = (44.6543412, 10.9011459)

# TODO: create presenters
templates = Jinja2Templates(directory="demo/templates")


class HomePage:
    @staticmethod
    async def execute(request):
        context = {"request": request}
        return templates.TemplateResponse("index.html", context)


class MapPage:
    def __init__(self, frequencies: FrequencyRepo):
        self._frequencies = frequencies

        # TODO: move this configuration to an external file
        self._map_config = {
            "location": AFOR_COORDINATES,
            "zoom_start": 14,
            "tiles": "Stamen Toner Background",
        }

    async def execute(self, request):
        _map = folium.Map(**self._map_config)
        for place in self._frequencies.places:
            frequencies = self._frequencies.fetch_frequency_table(place)

            cloud = WordCloud(background_color=None, mode="RGBA")
            cloud.generate_from_frequencies(frequencies)

            svg = cloud.to_svg()
            icon = folium.features.DivIcon(html=svg)
            marker = folium.Marker(place, icon=icon)

            marker.add_to(_map)

        context = {
            "map": _map._repr_html_(),  # or map.get_root().render()
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
