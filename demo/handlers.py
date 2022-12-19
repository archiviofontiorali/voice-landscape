from starlette.templating import Jinja2Templates

from . import presenters
from .system.types import Case, Handler

templates = Jinja2Templates(directory="templates")


class PageHandler(Handler):
    async def __call__(self, request):
        return await self.case.execute(request, self.presenter)


class APIHandler(Handler):
    async def __call__(self, request):
        return await self.case.execute(request, self.presenter)
