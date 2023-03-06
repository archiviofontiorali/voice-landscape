from typing import Literal

from starlette.routing import Route

from .types import Handler

Method = Literal["GET", "POST"]


def route(path: str, endpoint: Handler, method: Method = "GET", **kwargs) -> Route:
    endpoint = getattr(endpoint, method.lower(), endpoint.__call__)
    return Route(path, endpoint=endpoint, methods=[method], **kwargs)


def get(path: str, endpoint: Handler, **kwargs):
    return route(path, endpoint, "GET", **kwargs)


def post(path: str, endpoint: Handler, **kwargs):
    return route(path, endpoint, "POST", **kwargs)
