import logging

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save
from loguru import logger


class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "website"

    def ready(self):
        from . import models, signals

        # Send loguru logging to python standard logging library (managed by Django)
        logger.add(PropagateHandler(), level=settings.LOGURU_LOG_LEVEL)

        # signal: update frequencies on Share creation
        post_save.connect(
            signals.on_share_creation_update_frequencies, sender=models.Share
        )
