from typing import Iterable, List

from .constants import PLACES

Coordinates = tuple[float, float]


class FrequencySQLRepo:
    places: Iterable[Coordinates]

    def __init__(self, db):
        self._db = db
        self._table = "frequencies"
        self._keys = ", ".join(
            [
                "latitude FLOAT8 NOT NULL",
                "longitude FLOAT8 NOT NULL",
                "word TEXT NOT NULL",
                "frequency INT DEFAULT 1",
                "PRIMARY KEY(latitude, longitude, word)",
            ]
        )

        self._coordinates = list(PLACES.keys())

    async def init_db(self):
        await self._db.create_table(self._table, self._keys)

    @property
    def places(self) -> Iterable[Coordinates]:
        return self._coordinates

    async def update_frequency(self, place: Coordinates, key: str):
        values = dict(latitude=place[0], longitude=place[1], word=key)
        query = (
            f"INSERT INTO {self._table}(latitude, longitude, word) "
            "VALUES (:latitude, :longitude, :word) "
            "ON CONFLICT (latitude, longitude, word) "
            "DO UPDATE SET frequency = frequencies.frequency + 1"
        )
        await self._db.execute(query, **values)

    async def fetch_frequency_table(self, place: Coordinates) -> List[tuple]:
        values = dict(latitude=place[0], longitude=place[1])
        query = (
            f"SELECT word, frequency FROM {self._table} "
            "WHERE latitude=:latitude AND longitude=:longitude"
        )
        return await self._db.fetch_all(query, **values)
