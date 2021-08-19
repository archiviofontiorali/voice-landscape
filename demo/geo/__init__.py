import math
from typing import List, Tuple, Iterable

import geopy.distance
from wordcloud import WordCloud

from demo.system.structures import FrequencyDict

Coordinates = Tuple[float, float]


class PlacesDict(dict):
    def __init__(self, places: List[Coordinates]):
        super().__init__()

        for place in places:
            self.setdefault(place, FrequencyDict())

    def increment(self, place: Coordinates, key):
        self[place].increment(key)

    def increment_nearest_place(self, target: Coordinates, key):
        nearest, _distance = find_nearest_place(target, self.keys())
        self.increment(nearest, key)


def find_nearest_place(
    target: Coordinates, places: Iterable[Coordinates]
) -> Tuple[Coordinates, float]:
    near, distance = None, math.inf
    for place in places:
        new_distance = geopy.distance.geodesic(target, place).m
        if new_distance < distance:
            near, distance = place, new_distance
    return near, distance


def prepare_marker(place, frequency_repo) -> Tuple[List[float], str]:
    frequencies = frequency_repo.fetch_frequency_table(place)

    cloud = WordCloud(background_color=None, mode="RGBA")
    cloud.generate_from_frequencies(frequencies)

    svg = cloud.to_svg()
    return list(place), svg
