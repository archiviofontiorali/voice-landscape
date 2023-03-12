import sqlalchemy
import sqlmodel
from sqlmodel import SQLModel


class Place(SQLModel, table=True):
    __table_args__ = (sqlalchemy.UniqueConstraint("slug"),)

    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    slug: str
    latitude: float
    longitude: float


class Landscape(SQLModel, table=True):
    __table_args__ = (
        sqlalchemy.UniqueConstraint("slug"),
        sqlalchemy.UniqueConstraint("enabled"),
    )

    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    slug: str
    center: int | None = sqlmodel.Field(default=None, foreign_key="place.id")
    enabled: bool | None


class Voice(SQLModel, table=True):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    word: str
