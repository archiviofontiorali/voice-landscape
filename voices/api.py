from abc import ABC

import sqlmodel
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from .db import models
from .db.database import Database


class API(ABC):
    model: type[models.SQLModel]

    def __init__(self, db: Database):
        self.db = db

    async def get(self) -> JSONResponse:
        query = sqlmodel.select(self.model)
        return self.db.fetchall(query)

    async def post(self, request: dict) -> JSONResponse:
        raise HTTPException(501)

    async def update(self, request: dict) -> JSONResponse:
        raise HTTPException(501)

    async def delete(self, request: dict) -> JSONResponse:
        raise HTTPException(501)


class VoiceAPI(API):
    model = models.Voice
