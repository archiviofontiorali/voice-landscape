"""A Django script to add some shares to a demo instance

Example:

    (.venv)$ python manage.py runscript add_demo_share

"""

import random
import re

from django.conf import settings
from django.contrib.gis.geos import Point
from loguru import logger
from tqdm import tqdm

from .. import models

SHARE_PATH = settings.BASE_DIR / ".data" / "shares.txt"

TEXT_ROW_RE = re.compile(r"[A-Za-z]")


def save_share(location: Point, message: str, landscape: models.Landscape):
    defaults = {"location": location, "message": message, "landscape": landscape}
    share = models.Share(**defaults)
    share.full_clean()
    share.save()
    logger.debug(f"Created Share: {share}")
    return share


def run():
    if not (path := SHARE_PATH).exists():
        print(
            f"File {SHARE_PATH} not exists, please add a text file which lines are "
            "the shares you want to add (rows not containing text are skipped)"
        )
        quit()

    with path.open("rt") as fp:
        shares = fp.readlines()

    landscape = models.Landscape.visible_objects.get_default()
    places = list(landscape.places.all())

    for message in tqdm(shares):
        if not TEXT_ROW_RE.match(message):
            continue

        point = random.choice(places).location

        lat = point.x + random.gauss(0, 0.5)
        lon = point.y + random.gauss(0, 0.5)
        location = Point(x=lon, y=lat)

        save_share(location, message, landscape)
