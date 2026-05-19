import numpy as np
from django.contrib.gis.geos import Point

type MercatorCoordinates = tuple[float, float]
type Coordinates = list[float]


def mercator_longitude(longitude: float):
    """Convert a classic longitude to mercator projection"""
    return longitude * (6378137 * np.pi / 180.0)


def mercator_latitude(latitude: float) -> float:
    """Convert a classic latitude to mercator projection"""
    return np.log(np.tan((90 + latitude) * np.pi / 360.0)) * 6378137


def mercator_coordinates(latitude: float, longitude: float) -> MercatorCoordinates:
    """Convert classic coordinates to a mercator projection"""
    x = mercator_longitude(longitude)
    y = mercator_latitude(latitude)
    return x, y


def coordinates(point: Point) -> Coordinates:
    return [point.y, point.x]
