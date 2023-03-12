import sqlmodel.engine

from .. import settings
from . import models


class Database:
    def __init__(
        self, database: str = settings.DATABASE_URL, debug: bool = settings.DEBUG
    ):
        self.database = database
        self.debug = debug

        connect_args = {}
        if self.database.startswith("sqlite://"):
            connect_args = {"check_same_thread": False}

        self.engine = sqlmodel.create_engine(
            database, echo=debug, connect_args=connect_args
        )

    def create_tables(self):
        models.SQLModel.metadata.create_all(self.engine)

    def fetchall(self, query):
        with sqlmodel.Session(self.engine) as session:
            return session.exec(query).fetchall()

    def fetch(self, query):
        with sqlmodel.Session(self.engine) as session:
            return session.exec(query).first()
