import numpy as np
from django.contrib.gis.geos import Point


def mercator_longitude(longitude: float):
    """Convert a classic longitude to mercator projection"""
    return longitude * (6378137 * np.pi / 180.0)


def mercator_latitude(latitude: float) -> float:
    """Convert a classic latitude to mercator projection"""
    return np.log(np.tan((90 + latitude) * np.pi / 360.0)) * 6378137


def mercator_coordinates(latitude: float, longitude: float) -> tuple[float, float]:
    """Convert classic coordinates to a mercator projection"""
    x = mercator_longitude(longitude)
    y = mercator_latitude(latitude)
    return x, y


def coordinates(point: Point) -> list[float, float]:
    return [point.y, point.x]
