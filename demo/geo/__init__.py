import math
from typing import List, Tuple

import geopy.distance
from wordcloud import WordCloud

Coordinates = Tuple[float, float]


def find_nearest_place(
    target: Coordinates, places: List[Coordinates]
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
