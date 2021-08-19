from typing import Iterable

import folium
# from loguru import logger

from .constants import FOLIUM_MAP_CONFIG
from .geo import Coordinates, PlacesDict, prepare_marker
from .services import SQLite

# TODO: with bisect module and custom structure it's possible to improve performance


class FrequencyDictRepo:
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


class FrequencySQLRepo:
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

        self._coordinates = [(44.6543412, 10.9011459)]

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


class FoliumMapRepo:
    _map: folium.Map

    def __init__(self):
        self._config = FOLIUM_MAP_CONFIG
        self._map = folium.Map(**self._config)

    def update_map(self, frequency_repo):
        self._map = folium.Map(**self._config)
        for place in frequency_repo.places:
            _, svg = prepare_marker(place, frequency_repo)
            icon = folium.features.DivIcon(html=svg)
            marker = folium.Marker(place, icon=icon)

            marker.add_to(self._map)

    @property
    def map(self):
        # return self._map.get_root().render()
        return self._map._repr_html_()
