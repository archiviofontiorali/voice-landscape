from django.apps import AppConfig
from django.db.models.signals import post_save
from loguru import logger


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "website"

    def ready(self):
        from . import loggers, models, signals

        # Send loguru logging to python standard logging library (managed by Django)
        logger.add(loggers.PropagateHandler())
