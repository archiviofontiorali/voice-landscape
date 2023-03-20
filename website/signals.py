import spacy.symbols
from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from loguru import logger

from . import models

try:
    nlp = spacy.load(settings.SPACY_MODEL_NAME)
except IOError:
    spacy.cli.download(settings.SPACY_MODEL_NAME)
    nlp = spacy.load(settings.SPACY_MODEL_NAME)


def on_share_creation_update_frequencies(
    sender, instance: models.Share, created, **kwargs
):
    place = (
        models.Place.objects.annotate(distance=Distance("location", instance.location))
        .order_by("distance")
        .first()
    )

    for token in nlp(instance.message):
        if token.pos in settings.SPACY_VALID_TOKENS:
            wf, created = models.WordFrequency.objects.get_or_create(
                place=place, word=token.lemma_.lower()
            )
            wf.frequency = F("frequency") + 1
            wf.save()
