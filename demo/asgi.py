from loguru import logger
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def ping(request):
    response = "Pong!"
    logger.info(response)
    return PlainTextResponse(response)


async def fetch_text(request):
    pass


async def generate_map(request):
    pass


routes = [
    Route("/ping", endpoint=ping),
    Route("/send", endpoint=fetch_text),
    Route("/map", endpoint=generate_map),
]

app = Starlette(debug=True, routes=routes)
