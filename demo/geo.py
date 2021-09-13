import math
from typing import Iterable, List, Tuple

import geopy.distance
from wordcloud import WordCloud

from demo.system.structures import FrequencyDict

from .models import Coordinates, Place


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


# TODO: DEPRECATED, remove WordCloud after disposal
def prepare_marker(place, frequency_repo) -> Tuple[List[float], str]:
    frequencies = frequency_repo.fetch_frequency_table(place)

    cloud = WordCloud(
        background_color=None,
        mode="RGBA",
        color_func=lambda *args, **kwargs: "rgba(0,0,0,.7)",
        max_words=10,
    )
    if frequencies:
        cloud.generate_from_frequencies(frequencies)
    else:
        cloud.generate("voce")

    svg = cloud.to_svg()
    return list(place), svg


def prepare_map_frequencies(frequency_repo) -> list:
    result = []
    for place in frequency_repo.places:
        frequencies = frequency_repo.fetch_frequency_table(place)
        max_frequency = max(frequencies.values())
        for key in frequencies:
            frequencies[key] /= max_frequency
        obj = Place(coordinates=place, frequencies=frequencies).to_dict()
        result.append(obj)
    return result
