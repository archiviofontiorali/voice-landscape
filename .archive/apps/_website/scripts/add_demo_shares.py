"""A Django script to add some shares to a demo instance

Example:

    (.venv)$ python manage.py runscript add_demo_share

"""

import random
import re

from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils import timezone
from tqdm import tqdm

from .. import models

SHARE_PATH = settings.BASE_DIR / ".data" / "shares.txt"

TEXT_ROW_RE = re.compile(r"[A-Za-z]")


def random_timestamp(delta=1440):
    minutes = round(random.gauss(0, delta))
    return timezone.now() + timezone.timedelta(minutes=minutes)


def save_share(location: Point, message: str, landscape: models.Landscape):
    share = models.Share(
        location=location,
        message=message,
        landscape=landscape,
        timestamp=random_timestamp(),
    )
    share.full_clean()
    share.save()
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
    places = [p.coordinates for p in landscape.places.all()]

    for message in tqdm(shares):
        if not TEXT_ROW_RE.match(message):
            continue

        lat, lon = random.choice(places)
        location = Point(x=lon, y=lat)

        save_share(location, message, landscape)
