from starlette.templating import Jinja2Templates

from .system.types import Handler

templates = Jinja2Templates(directory="templates")


class PageHandler(Handler):
    async def __call__(self, request):
        return await self.case.execute(request, self.presenter)


class APIHandler(Handler):
    async def __call__(self, request):
        return await self.case.execute(request, self.presenter)
