import re

import spacy.symbols
from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from loguru import logger

from . import models
from .tools.blacklist import BlackList

# For more info see:
# https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
HTML_TAG_RE = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")

try:
    nlp = spacy.load(settings.SPACY_MODEL_NAME)
except IOError:
    logger.info("Spacy model not found downloading it")
    spacy.cli.download(settings.SPACY_MODEL_NAME)
    nlp = spacy.load(settings.SPACY_MODEL_NAME)

blacklist = BlackList()
if path := settings.BLACKLIST_PATH:
    blacklist.load_file(path)


def on_share_creation_update_frequencies(
    sender, instance: models.Share, created, **kwargs
):
    if not created:
        return

    place = (
        models.Place.objects.filter(landscape=instance.landscape)
        .annotate(distance=Distance("location", instance.location))
        .order_by("distance")
        .first()
    )

    logger.debug(
        f"Receive share near [{place}], update WordFrequency "
        f"(message: {instance.message})"
    )

    for token in nlp(instance.message):
        if token.pos not in settings.SPACY_VALID_TOKENS:
            logger.debug(
                f"Skip token {token} with pos ({token.pos}) "
                f"'{spacy.explain(token.pos_)}'"
            )
            continue

        text = HTML_TAG_RE.sub("", token.lemma_).strip().lower()

        word, created = models.Word.objects.get_or_create(text=text)
        if created and word.text in blacklist:
            word.visible = False
        word.full_clean()
        word.save()

        wf, _ = models.WordFrequency.objects.get_or_create(place=place, word=word)
        wf.frequency = F("frequency") + 1
        wf.save()

        if created:
            logger.debug(f"Create counter for {word}")
        else:
            logger.debug(f"Increment counter for {word}")
