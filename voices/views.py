from starlette.templating import Jinja2Templates

from . import settings

template_engine = Jinja2Templates(directory=settings.TEMPLATES)


class Template:
    def __init__(self, template_name: str):
        self.template_name = template_name

    def render(self, context: dict):
        template_engine.TemplateResponse(self.template_name, context)
