import numpy as np
import spacy
from loguru import logger
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

nlp = spacy.load("it_core_news_sm")
# nlp = spacy.load("en_core_web_sm")


class Frequencies:
    def __init__(self):
        self._nlp = spacy.load("it_core_news_sm")
        self._places = [(0.0, 0.0), (1.0, 1.0)]
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

    def get_top_token(self, addr, k=5):
        freq = self._frequencies[addr]
        top = sorted(freq.items(), key=lambda d: d[1], reverse=True)
        return top[:5]

    @property
    def valid_addresses(self):
        return self._places


frequencies = Frequencies()


async def ping(request):
    response = "Pong!"
    logger.info(response)
    return PlainTextResponse(response)


async def fetch_text(request):
    data = await request.json()

    gps = data.get("gps", None)
    text = data.get("text", None)
    if text is None or gps is None:
        return JSONResponse("Not valid")
    else:
        logger.debug(f"[{gps[0]}, {gps[1]}] {text}")

    place = frequencies.load_text(text, gps)  # doc = nlp(text)
    return JSONResponse(f"updated {place}")


async def generate_map(request):
    result = []
    for address in frequencies.valid_addresses:
        words = frequencies.get_top_token(address)
        result.append(dict(address=address, words=words))
    return JSONResponse(result)


routes = [
    Route("/ping", endpoint=ping),
    Route("/send", endpoint=fetch_text, methods=["POST"]),
    Route("/map", endpoint=generate_map),
]

app = Starlette(debug=True, routes=routes)
