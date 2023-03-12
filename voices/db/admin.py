import sqladmin

from . import models
from .models import Voice


class VoiceAdmin(sqladmin.ModelView, model=Voice):
    column_list = [Voice.id, Voice.word]


class PlaceAdmin(sqladmin.ModelView, model=models.Place):
    column_list = [models.Place.slug, models.Place.latitude, models.Place.longitude]


class LandscapeAdmin(sqladmin.ModelView, model=models.Landscape):
    column_list = [models.Landscape.slug, models.Landscape.center]
