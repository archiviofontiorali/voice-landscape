"""This script fill the db with demo data."""

import django.db.utils
import django.utils.text
from decouple import config  # noqa
from django.contrib.gis.geos import Point
from loguru import logger
from tqdm import tqdm

from website import models

places = {
    # Festival Filosofia 2019
    "ff_2019": [
        (44.65461615128406, 10.901229167243947, "AFOr | Archivio delle Fonti Orali"),
        (44.644092562898706, 10.931416796520214, "Teatro Storchi"),
        (44.64076056627556, 10.925855204224685, "Casa del Mutilato"),
        (44.64268450564671, 10.927843757773337, "Monastero di San Pietro"),
        (44.64378439331217, 10.923000303364157, "Piazzale Redecocca"),
        (44.64320862552364, 10.924562225569376, "Complesso San Paolo"),
        (44.643287245670166, 10.920327858710017, "Seminario Metropolitano"),
        (44.64490308389011, 10.925538865059846, "Chiesa San Bartolomeo"),
        (44.64538532829409, 10.92474709775705, "Centro Storico Via Selmi 27"),
        (44.64637903460112, 10.927300330551235, "Fondazione Collegio San Carlo"),
        (44.64726495763729, 10.928124802602303, "Cantore Galleria Antiquaria"),
        (44.64895556021473, 10.928913388481552, "Piazza Roma"),
        (44.64851834986531, 10.927779977375678, "ArteSì Galleria d'Arte Contemporanea"),
        (44.64960205700249, 10.917826093129312, "Civico Planetario F. Martino"),
        (44.648611683830424, 10.921297460510141, "Palazzo dei Musei"),
        (44.647563509765625, 10.921629093093763, "Palazzo Ferrari Moreni"),
        (44.64797936822664, 10.923185909280745, "Metronom"),
        (44.64682739314981, 10.925702430899005, "Musei del Duomo"),
        (
            44.647266321450616,
            10.924308814124794,
            "Dip. di studi linguistici e culturali",
        ),
        (44.64889538513829, 10.924628946332877, "Grandezze & Meraviglie"),
        (44.64960871352613, 10.92411238719445, "Chiesa di Santa Maria della Pomposa"),
        (44.654349533832914, 10.919545596245719, "Palestra Panaro"),
        (44.65108757903913, 10.928966300288407, "Fondazione San Filippo Neri"),
        (44.6497421887335, 10.932770905604967, "Giardini Ducali"),
        (44.64571849202709, 10.92991325127264, "Laboratorio di Poesia"),
        (44.65150093334555, 10.933805225452874, "Teatro Tempio"),
        (44.645142067669966, 10.926580987228016, "Consorzio Creativo"),
    ],
    # Scuola di Storia Orale (25-26/03/2023)
    "sso_2023": [
        (44.6543937853751, 10.901187414574565, "#Ovestlab"),
    ],
}


def run():
    place_id = config("DEMO_REFERENCE", default="ff_2019")
    if place_id not in places:
        raise Exception(f"DEMO_REFERENCE can be only one of {', '.join(places)}")

    for lat, lon, title in (_places := places[place_id]):
        slug = django.utils.text.slugify(title)
        place, created = models.Place.objects.get_or_create(
            slug=slug, title=title, location=Point(x=lon, y=lat)
        )

        if created:
            place.save()
            logger.info(f"Added place {place}")
        else:
            logger.info(f"Place with slug {slug} already exists")

        if config("DEMO_ADD_WORDS", cast=bool, default=True):
            logger.info(f"Adding some test words to place {place.title}")
            for _ in tqdm(range(10)):
                models.WordFrequency.create_random(place)
