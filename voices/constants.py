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
    # (44.644092562898706, 10.931416796520214): "Teatro Storchi",
    # (44.64076056627556, 10.925855204224685): "Casa del Mutilato",
    # (44.64268450564671, 10.927843757773337): "Monastero di San Pietro",
    # (44.64378439331217, 10.923000303364157): "Piazzale Redecocca",
    # (44.64320862552364, 10.924562225569376): "Complesso San Paolo",
    # (44.643287245670166, 10.920327858710017): "Seminario Metropolitano",
    # # (44.64490308389011, 10.925538865059846): "Chiesa San Bartolomeo",
    # (44.64538532829409, 10.92474709775705): "Centro Storico Via Selmi 27",
    # # (44.64637903460112, 10.927300330551235): "Fondazione Collegio San Carlo",
    # (44.64726495763729, 10.928124802602303): "Cantore Galleria Antiquaria",
    # (44.64895556021473, 10.928913388481552): "Piazza Roma",
    # (44.64851834986531, 10.927779977375678): "ArteSì Galleria d'Arte Contemporanea",
    # (44.64960205700249, 10.917826093129312): "Civico Planetario F. Martino",
    # (44.648611683830424, 10.921297460510141): "Palazzo dei Musei",
    # (44.647563509765625, 10.921629093093763): "Palazzo Ferrari Moreni",
    # (44.64797936822664, 10.923185909280745): "Metronom",
    # (44.64682739314981, 10.925702430899005): "Musei del Duomo",
    # (44.647266321450616, 10.924308814124794): "Dip. di studi linguistici e culturali",
    # (44.64889538513829, 10.924628946332877): "Grandezze & Meraviglie",
    # (44.64960871352613, 10.92411238719445): "Chiesa di Santa Maria della Pomposa",
    # (44.654349533832914, 10.919545596245719): "Palestra Panaro",
    # (44.65108757903913, 10.928966300288407): "Fondazione San Filippo Neri",
    # (44.6497421887335, 10.932770905604967): "Giardini Ducali",
    # (44.64571849202709, 10.92991325127264): "Laboratorio di Poesia",
    # (44.65150093334555, 10.933805225452874): "Teatro Tempio",
    # (44.645142067669966, 10.926580987228016): "Consorzio Creativo",
}

for i, p in enumerate(points):
    PLACES[(p[0], p[1])] = f"place #{i}"
