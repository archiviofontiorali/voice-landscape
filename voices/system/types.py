from abc import ABC

from starlette.requests import Request


class Case(ABC):
    async def execute(self, request: Request, presenter) -> dict:
        pass


class Handler(ABC):
    case: Case

    def __init__(self, case: Case, presenter):
        self.case = case
        self.presenter = presenter

    async def __call__(self, request: Request):
        pass
