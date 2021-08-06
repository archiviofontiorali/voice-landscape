import spacy
from loguru import logger
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

nlp = spacy.load("it_core_news_sm")
# nlp = spacy.load("en_core_web_sm")


async def ping(request):
    response = "Pong!"
    logger.info(response)
    return PlainTextResponse(response)


async def fetch_text(request):
    data = await request.json()
    text = data.get("text", None)
    gps = data.get("gps", None)

    if text is None or gps is None:
        return JSONResponse("Not valid")

    logger.debug(f"[{gps[0]}, {gps[1]}] {text}")

    doc = nlp(text)
    freq = dict()

    for token in doc:
        logger.debug(f"{token.text:12} {token.lemma_:12} {token.pos_:5} {token.tag_}")
        if token.tag_ not in ("V", "S"):
            continue

        try:
            freq[token.lemma_] += 1
        except KeyError:
            freq[token.lemma_] = 1

    top = sorted(freq.items(), key=lambda d: d[1], reverse=True)
    return JSONResponse(top)


async def generate_map(request):
    pass


routes = [
    Route("/ping", endpoint=ping),
    Route("/send", endpoint=fetch_text, methods=["POST"]),
    Route("/map", endpoint=generate_map),
]

app = Starlette(debug=True, routes=routes)
