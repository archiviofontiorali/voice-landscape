from abc import ABC

from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates

from . import settings

template_engine = Jinja2Templates(directory=settings.TEMPLATES)


class Template(ABC):
    template: str

    async def get(self, request: dict):
        return template_engine.TemplateResponse(self.template, {"request": request})


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


class Showcase(Template):
    template = "showcase.html"


class Share(Template):
    template = "share.html"
