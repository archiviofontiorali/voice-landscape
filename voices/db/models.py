import sqlmodel
from sqlmodel import SQLModel


class Voice(SQLModel, table=True):
    id: int | None = sqlmodel.Field(default=True, primary_key=True)
    word: str
