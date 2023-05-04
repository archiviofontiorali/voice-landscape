import spacy.symbols
from django.conf import settings
from django.db.models import F
from loguru import logger

from . import models

try:
    nlp = spacy.load(settings.SPACY_MODEL_NAME)
except IOError:
    logger.info("Spacy model not found downloading it")
    spacy.cli.download(settings.SPACY_MODEL_NAME)
    nlp = spacy.load(settings.SPACY_MODEL_NAME)


def on_share_creation_update_frequencies(
    sender, instance: models.Share, created, **kwargs
):
    if not created:
        return

    place = models.Place.get_nearest(instance.location)
    logger.debug(
        f"Add share near '{place}', try to update frequencies "
        f"(message: {instance.message})"
    )

    for token in nlp(instance.message):
        message = f"token {token} with pos ({token.pos}) '{spacy.explain(token.pos_)}'"
        if token.pos not in settings.SPACY_VALID_TOKENS:
            logger.debug(f"Skip {message}")
            continue

        word = token.lemma_
        wf, created = models.WordFrequency.objects.get_or_create(place=place, word=word)
        wf.frequency = F("frequency") + 1
        wf.save()

        if created:
            logger.debug(f"Found {message}, create counter for {word}")
        else:
            logger.debug(f"Found {message}, increment counter for {word}")
