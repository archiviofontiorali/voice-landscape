from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save
from loguru import logger


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "voices.website"

    def ready(self):
        from . import loggers, models, signals

        # Send loguru logging to python standard logging library (managed by Django)
        logger.add(
            loggers.PropagateHandler(), level="DEBUG" if settings.DEBUG else "WARNING"
        )

        # signal: update frequencies on Share creation
        post_save.connect(
            signals.on_share_creation_update_frequencies, sender=models.Share
        )
