import matplotlib.pyplot as plt
import numpy as np
import spacy
from loguru import logger
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse
from starlette.routing import Route
from wordcloud import WordCloud
from starlette.templating import Jinja2Templates

import folium
import folium.features

nlp = spacy.load("it_core_news_sm")
# nlp = spacy.load("en_core_web_sm")

templates = Jinja2Templates(directory="demo/templates")


class Frequencies:
    # NOTE: with bisect module and custom structure it's possible to improve performance

    def __init__(self):
        self._nlp = spacy.load("it_core_news_sm")
        self._places = [(44.6543412, 10.9011459)]
        self._frequencies = {coord: dict() for coord in self._places}

    def _find_nearest_place(self, coord: tuple):
        near, distance = None, np.inf
        for p in self._places:
            d = np.linalg.norm(np.array(p) - np.array(coord))
            if d < distance:
                near, distance = p, d
        return near, distance

    def load_text(self, text, gps):
        doc = self._nlp(text)
        near, _ = self._find_nearest_place(gps)
        freq = self._frequencies[near]

        for token in doc:
            if token.tag_ in ("V", "S"):
                try:
                    freq[token.lemma_] += 1
                except KeyError:
                    freq[token.lemma_] = 1

        return near

    def get_top_token(self, address, k=5):
        freq = self._frequencies[address]
        top = sorted(freq.items(), key=lambda d: d[1], reverse=True)
        return top[:k]

    def create_word_cloud(self, address) -> str:
        cloud = WordCloud(background_color=None, mode="RGBA")
        cloud.generate_from_frequencies(frequencies._frequencies[address])
        return cloud.to_svg()

    @property
    def valid_addresses(self):
        return self._places


frequencies = Frequencies()


async def ping(request):
    response = "Pong!"
    logger.info(response)
    return PlainTextResponse(response)


async def fetch_text(request):
    data = await request.form()

    loc_x, loc_y = data.get("loc-x", None), data.get("loc-y", None)
    loc_x, loc_y = map(float, (loc_x, loc_y))
    text = data.get("text", None)

    if text is None or loc_x is None or loc_y is None:
        return JSONResponse("Not valid")
    else:
        logger.debug(f"[{loc_x}, {loc_y}] {text}")

    place = frequencies.load_text(text, (loc_x, loc_y))
    logger.debug(f"updated {place}")


async def generate_map(request):
    afor = [44.6543412, 10.9011459]
    map = folium.Map(location=afor, zoom_start=14, tiles="Stamen Toner Background")

    for address in frequencies.valid_addresses:
        svg = frequencies.create_word_cloud(address)
        map.add_child(
            folium.Marker(
                address,
                icon=folium.features.DivIcon(
                    html=svg,
                ),
            )
        )

    context = {
        "map": map._repr_html_(),  # or map.get_root().render()
        "request": request,
    }

    return templates.TemplateResponse("map.html", context)


async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})


async def sharepage(request):
    if request.method == "POST":
        await fetch_text(request)
    return templates.TemplateResponse("share.html", {"request": request})


routes = [
    Route("/", endpoint=homepage),
    Route("/share", endpoint=sharepage, methods=["GET", "POST"]),
    Route("/map", endpoint=generate_map),
    Route("/ping", endpoint=ping),
]

app = Starlette(debug=True, routes=routes)
