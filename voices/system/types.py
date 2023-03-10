from abc import ABC, abstractmethod
from typing import Any

from starlette.requests import Request


class Case(ABC):
    @abstractmethod
    async def execute(self, request: Request, presenter) -> dict:
        pass


class GenericHandler(ABC):
    @abstractmethod
    async def __call__(self, request: Request):
        pass


class Handler(GenericHandler, ABC):
    case: Case
    presenter: Any

    def __init__(self, case: Case, presenter):
        self.case = case
        self.presenter = presenter
