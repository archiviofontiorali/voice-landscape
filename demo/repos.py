from abc import ABC
from typing import Iterable

from .geo import Coordinates, PlacesDict
from .services import SQLite

# from loguru import logger


# TODO: with bisect module and custom structure it's possible to improve performance


class FrequencyRepo(ABC):
    places: Iterable[Coordinates]

    def update_frequency(self, place: Coordinates, key: str):
        pass

    def fetch_frequency_table(self, place: Coordinates) -> dict:
        pass


class FrequencyDictRepo(FrequencyRepo):
    def __init__(self):
        self._coordinates = [(44.6543412, 10.9011459)]
        self._data = PlacesDict(self._coordinates)

    @property
    def places(self) -> Iterable[Coordinates]:
        return self._data.keys()

    def update_frequency(self, place: Coordinates, key: str):
        self._data.increment(place, key)

    def fetch_frequency_table(self, place: Coordinates) -> dict:
        return self._data.get(place)


class FrequencySQLRepo(FrequencyRepo):
    def __init__(self, sql_db: SQLite):
        self._db = sql_db
        self._table = "frequencies"
        self._keys = ", ".join(
            [
                "latitude REAL NOT NULL",
                "longitude REAL NOT NULL",
                "word TEXT NOT NULL",
                "frequency INT DEFAULT 1",
                "PRIMARY KEY(latitude, longitude, word)",
            ]
        )

        self._coordinates = [
            (44.6543412, 10.9011459),
            (44.654110667970976, 10.898906959317424),
        ]

        self._db.create_table(self._table, self._keys)

    @property
    def places(self) -> Iterable[Coordinates]:
        return self._coordinates

    def update_frequency(self, place: Coordinates, key: str):
        query = (
            f"INSERT INTO {self._table} (latitude, longitude, word) "
            "VALUES (:latitude, :longitude, :word) "
            "ON CONFLICT(latitude, longitude, word) DO UPDATE SET frequency=frequency+1"
        )
        self._db.execute(query, latitude=place[0], longitude=place[1], word=key)

    def fetch_frequency_table(self, place: Coordinates) -> dict:
        query = (
            f"SELECT word, frequency FROM {self._table} "
            "WHERE latitude=:latitude AND longitude=:longitude"
        )
        result = self._db.execute(query, latitude=place[0], longitude=place[1])
        return dict(result.fetchall())
