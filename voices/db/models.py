import sqlmodel
from sqlmodel import SQLModel


class Voice(SQLModel, table=True):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    word: str
