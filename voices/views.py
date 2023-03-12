from abc import ABC

from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates

from . import constants, settings

template_engine = Jinja2Templates(directory=settings.TEMPLATES)


class Template(ABC):
    template: str

    def get_context(self):  # noqa
        return {}

    async def get(self, request: dict):
        context = self.get_context()
        context.setdefault("request", request)
        return template_engine.TemplateResponse(self.template, context)


class Static(ABC):
    filename: str

    async def get(self, request):
        return FileResponse(settings.STATIC_PATH / self.filename)


class Favicon(Static):
    filename = "favicon.ico"


class HomePage(Template):
    template = "index.html"


class Privacy(Template):
    template = "privacy.html"


class Map(Template):
    template = "map.html"

    def get_context(self):
        return {
            "center": [0, 0],  # TODO: move to db
            "places": [],
        }


class Showcase(Template):
    template = "showcase.html"


class Share(Template):
    template = "share.html"
