from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates


class JSON:
    @staticmethod
    def json(data):
        return JSONResponse(data)


class Template:
    def __init__(self, directory: str = "templates"):
        self.templates = Jinja2Templates(directory=directory)

    def render(self, template: str, context: dict):
        return self.templates.TemplateResponse(template, context)
