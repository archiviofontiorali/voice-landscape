import re

import spacy.symbols
from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from loguru import logger
from tqdm import tqdm

from .. import models

# For more info see:
# https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
HTML_TAG_RE = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")

try:
    nlp = spacy.load(settings.SPACY_MODEL_NAME)
except IOError:
    logger.info("Spacy model not found downloading it")
    spacy.cli.download(settings.SPACY_MODEL_NAME)
    nlp = spacy.load(settings.SPACY_MODEL_NAME)


def recalculate_share(instance: models.Share):
    place = (
        models.Place.objects.filter(landscape=instance.landscape)
        .annotate(distance=Distance("location", instance.location))
        .order_by("distance")
        .first()
    )

    instance.place = place
    instance.save()

    for token in nlp(instance.message):
        if token.pos not in settings.SPACY_VALID_TOKENS:
            continue

        text = HTML_TAG_RE.sub("", token.lemma_).strip().lower()

        word, created = models.Word.objects.get_or_create(text=text)
        instance.words.add(word)


def run():
    for share in tqdm(models.Share.objects.all()):
        recalculate_share(share)
