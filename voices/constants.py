import pathlib

import numpy as np
from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config(
    "DATABASE_URL",
    cast=str,
    default=f"sqlite://",
)

TEMPLATES = config("TEMPLATES", default="templates")

STATIC_PATH = pathlib.Path("www/")


AFOR_COORDINATES = (44.65461615128406, 10.901229167243947)
# CENTER_COORDINATES = (44.64686795312118, 10.925334855944921)
CENTER_COORDINATES = (44.64957553765551, 10.896377547935987)
MAP_PROVIDER_URL = (
    "https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.png"
)
MAP_PROVIDER_ATTRIBUTION = (
    'Map tiles by <a href="http://stamen.com">Stamen Design</a>, '
    '<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> '
    "&mdash; Map data &copy; "
    '<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
)

SHOWCASE_RELOAD_TIME = 5 * 60  # Time in seconds for refreshing

a = np.array([44.647728027899625, 10.88466746283678])
b = np.array([44.64159324683118, 10.902033051497972])
c = np.array([44.65583248401956, 10.903694945558476])
v1, v2 = b - a, c - a

N = 6
points = np.empty(((N + 1) * (N + 2) // 2, 2))
count = 0
for i in range(N + 1):
    for j in range(N - i + 1):
        points[count, :] = a + (i / N) * v1 + (j / N) * v2
        count += 1

PLACES = {
    # CENTER_COORDINATES: "centro modena",
    AFOR_COORDINATES: "AFOr | Archivio fonti orali",
}

for i, p in enumerate(points):
    PLACES[(p[0], p[1])] = f"place #{i}"
