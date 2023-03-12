from abc import ABC

from starlette.templating import Jinja2Templates

from . import settings

template_engine = Jinja2Templates(directory=settings.TEMPLATES)


class Template(ABC):
    template: str

    async def get(self, request: dict):
        return template_engine.TemplateResponse(self.template, {"request": request})


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
