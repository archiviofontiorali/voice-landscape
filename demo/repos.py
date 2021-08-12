from typing import List
import folium
from wordcloud import WordCloud

from .geo import Coordinates, find_nearest_place
from .services import FrequencyDict
from .constants import AFOR_COORDINATES


class FrequencyRepo:
    # TODO: places should be initialized by a method executed during app initialization
    # TODO: with bisect module and custom structure it's possible to improve performance
    # TODO: frequencies should be saved in an external database
    # TODO: FrequencyDict could be an utility structure rather than a service

    def __init__(self, service: FrequencyDict):
        self._service = service
        self._service.init_addresses([(44.6543412, 10.9011459)])

    @property
    def places(self) -> List[Coordinates]:
        return self._service.addresses

    def find_nearest_place(self, coord: Coordinates) -> Coordinates:
        return find_nearest_place(coord, self._service.addresses)[0]

    def update_frequency(self, place: Coordinates, key: str):
        self._service.increment(place, key)

    def fetch_frequency_table(self, place: Coordinates):
        return self._service.fetch_address(place)


class FoliumMapRepo:
    def __init__(self):
        self._config = {
            "location": AFOR_COORDINATES,
            "zoom_start": 14,
            "tiles": "Stamen Toner Background",
        }

    def generate_map(self, frequency_repo):
        _map = folium.Map(**self._config)
        for place in frequency_repo.places:
            frequencies = frequency_repo.fetch_frequency_table(place)

            cloud = WordCloud(background_color=None, mode="RGBA")
            cloud.generate_from_frequencies(frequencies)

            svg = cloud.to_svg()
            icon = folium.features.DivIcon(html=svg)
            marker = folium.Marker(place, icon=icon)

            marker.add_to(_map)

        return _map._repr_html_()  # or map.get_root().render()
