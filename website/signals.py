# import spacy
import spacy.symbols
from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

nlp = spacy.load(settings.SPACY_MODEL_NAME)


@receiver(post_save, sender=models.Share)
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
