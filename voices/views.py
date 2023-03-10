from abc import ABC

from starlette.templating import Jinja2Templates

from . import settings

template_engine = Jinja2Templates(directory=settings.TEMPLATES)


class Template(ABC):
    template: str

    async def render(self, request: dict):
        return template_engine.TemplateResponse(self.template, {"request": request})


class HomePage(Template):
    template = "index.html"
