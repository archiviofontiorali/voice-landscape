import pathlib

from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates

from . import constants, presenters
from .system.types import Case, GenericHandler, Handler

templates = Jinja2Templates(directory="templates")


class PageHandler(Handler):
    async def __call__(self, request):
        return await self.case.execute(request, self.presenter)


class APIHandler(Handler):
    async def __call__(self, request):
        return await self.case.execute(request, self.presenter)


class Static(GenericHandler):
    def __init__(
        self, file_name: str, static_path: pathlib.Path | str = constants.STATIC_PATH
    ):
        self._name = file_name
        self._path = pathlib.Path(static_path)

    async def __call__(self, request):
        return FileResponse(self._path / self._name)
