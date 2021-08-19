from typing import Iterable

import folium

from .constants import FOLIUM_MAP_CONFIG
from .geo import Coordinates, prepare_marker
from .geo import PlacesDict

# TODO: with bisect module and custom structure it's possible to improve performance
# TODO: frequencies should be saved in an external database


class FrequencyDictRepo:
    def __init__(self):
        self._coordinates = [(44.6543412, 10.9011459)]
        self._data = PlacesDict(self._coordinates)

    @property
    def places(self) -> Iterable[Coordinates]:
        return self._data.keys()

    def update_frequency(self, place: Coordinates, key):
        self._data.increment(place, key)

    def update_nearest_place(self, target: Coordinates, key):
        self._data.increment_nearest_place(target, key)

    def fetch_frequency_table(self, place: Coordinates) -> dict:
        return self._data.get(place)


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
