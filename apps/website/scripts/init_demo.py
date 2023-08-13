"""This script fill the db with demo data."""

import django.db.utils
import django.utils.text
from decouple import config  # noqa
from django.contrib.gis.geos import Point
from loguru import logger
from tqdm import tqdm

from .. import models

places = {
    # Festival Filosofia 2021
    "ff_2021": [
        (44.65461615128406, 10.901229167243947, "AFOr | Archivio delle Fonti Orali"),
        (44.64409256289870, 10.931416796520214, "Teatro Storchi"),
        (44.64076056627556, 10.925855204224685, "Casa del Mutilato"),
        (44.64268450564671, 10.927843757773337, "Monastero di San Pietro"),
        (44.64378439331217, 10.923000303364157, "Piazzale Redecocca"),
        (44.64320862552364, 10.924562225569376, "Complesso San Paolo"),
        (44.64328724567016, 10.920327858710017, "Seminario Metropolitano"),
        (44.64490308389011, 10.925538865059846, "Chiesa San Bartolomeo"),
        (44.64538532829409, 10.924747097757050, "Centro Storico Via Selmi 27"),
        (44.64637903460112, 10.927300330551235, "Fondazione Collegio San Carlo"),
        (44.64726495763729, 10.928124802602303, "Cantore Galleria Antiquaria"),
        (44.64895556021473, 10.928913388481552, "Piazza Roma"),
        (44.64851834986531, 10.927779977375678, "ArteSì Galleria d'Arte Contemporanea"),
        (44.64960205700249, 10.917826093129312, "Civico Planetario F. Martino"),
        (44.64861168383042, 10.921297460510141, "Palazzo dei Musei"),
        (44.64756350976562, 10.921629093093763, "Palazzo Ferrari Moreni"),
        (44.64797936822664, 10.923185909280745, "Metronom"),
        (44.64682739314981, 10.925702430899005, "Musei del Duomo"),
        (44.64726632145061, 10.924308814124794, "Dip. studi linguistici e culturali"),
        (44.64889538513829, 10.924628946332877, "Grandezze & Meraviglie"),
        (44.64960871352613, 10.924112387194450, "Chiesa di Santa Maria della Pomposa"),
        (44.65434953383291, 10.919545596245719, "Palestra Panaro"),
        (44.65108757903913, 10.928966300288407, "Fondazione San Filippo Neri"),
        (44.64974218873350, 10.932770905604967, "Giardini Ducali"),
        (44.64571849202709, 10.929913251272640, "Laboratorio di Poesia"),
        (44.65150093334555, 10.933805225452874, "Teatro Tempio"),
        (44.64514206766996, 10.926580987228016, "Consorzio Creativo"),
    ],
    # Scuola di Storia Orale (25-26/03/2023)
    "sso_2023": [
        (44.65460, 10.90104, "#Ovestlab"),
        (44.65905, 10.91090, "San Cataldo"),
        (44.66201, 10.93171, "Parco Vittime di Utoya"),
        (44.66356, 10.92692, "Campo Cesena"),
        (44.65292, 10.89572, "Diagonale verde - campo"),
        (44.65012, 10.88912, "Fine ciclabile"),
        (44.65040, 10.89507, "Alboni"),
        (44.65374, 10.90391, "Fratellanza"),
    ],
}


def run():
    place_id = config("DEMO_REFERENCE", default="sso_2023")
    if place_id not in places:
        raise Exception(
            f"DEMO_REFERENCE should be one of {', '.join(places)}, found {place_id}"
        )

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