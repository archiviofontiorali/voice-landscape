import re

import spacy
from django.conf import settings
from django.db.models import F
from loguru import logger
from spacy.cli.download import download

from . import models
from .tools.blacklist import BlackList

# For more info see:
# https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
HTML_TAG_RE = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")

try:
    nlp = spacy.load(settings.SPACY_MODEL_NAME)
except IOError:
    logger.info("Spacy model not found downloading it")
    download(settings.SPACY_MODEL_NAME)
    nlp = spacy.load(settings.SPACY_MODEL_NAME)

blacklist = BlackList()
if path := settings.BLACKLIST_PATH:
    blacklist.load_file(path)


def on_share_creation_update_frequencies(
    sender, instance: models.Share, created, **kwargs
):
    if not created:
        return

    logger.debug(f"Received share, update WordFrequency (message: {instance.message})")

    for token in nlp(instance.message):
        if token.pos not in settings.SPACY_VALID_TOKENS:
            logger.debug(
                f"Skip token {token} with pos ({token.pos}) "
                f"'{spacy.explain(token.pos_)}'"  # type: ignore
            )
            continue

        text = HTML_TAG_RE.sub("", token.lemma_).strip().lower()

        word, created = models.Word.objects.get_or_create(text=text)
        if created and word.text in blacklist:
            word.visible = False
        word.full_clean()
        word.save()

        instance.words.add(word)

        wf, _ = models.WordFrequency.objects.get_or_create(
            place=instance.place, word=word
        )
        wf.frequency = F("frequency") + 1
        wf.save()

        if created:
            logger.debug(f"Create counter for {word}")
        else:
            logger.debug(f"Increment counter for {word}")
