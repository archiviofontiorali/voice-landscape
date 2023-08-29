import random
import textwrap

from django.contrib.gis.db import models
from django.contrib.gis.db.models.aggregates import Union
from django.contrib.gis.db.models.functions import Centroid, Distance
from django.contrib.gis.geos import Point
from django.db.models import F, Max, Q, Sum
from django.utils.translation import gettext as _

from .fields import UniqueBooleanField
from .tools.geo import coordinates, mercator_coordinates


class LocationModel(models.Model):
    location = models.PointField()

    @property
    def latitude(self) -> float:
        return self.location.y

    @property
    def longitude(self) -> float:
        return self.location.x

    @property
    def coordinates(self) -> list[float, float]:
        return coordinates(self.location)

    @property
    def mercator_coordinates(self) -> tuple[float, float]:
        return mercator_coordinates(self.latitude, self.longitude)

    def __str__(self):
        return f"({self.latitude:.4f}, {self.longitude:.4f})"

    class Meta:
        abstract = True


class TitledModel(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Share(LocationModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=500)
    landscape = models.ForeignKey("Landscape", on_delete=models.CASCADE)

    def __str__(self):
        message = textwrap.shorten(self.message, width=12, placeholder="...")
        return f"{super().__str__()} [{message}]"


class Place(LocationModel):
    slug = models.SlugField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)

    description = models.TextField(max_length=500, blank=True)

    @classmethod
    def get_nearest(cls, location: Point) -> "Place":
        return (
            cls.objects.annotate(distance=Distance("location", location))
            .order_by("distance")
            .first()
        )

    def get_frequencies(self, min_frequency: int = 3) -> list[list[str, float]]:
        """Return a list of [word, frequency] with the latest normalized"""
        frequencies = self.word_frequencies.filter(
            frequency__gte=min_frequency, word__visible=True
        )
        max_ = frequencies.aggregate(Max("frequency"))["frequency__max"]
        return [[wf.word.text, wf.frequency / max_] for wf in frequencies]

    def __str__(self):
        if self.title:
            return self.title
        if self.slug:
            return self.slug
        return LocationModel.__str__(self)


class Word(models.Model):
    text = models.CharField(max_length=100, unique=True)
    visible = models.BooleanField(
        default=True,
        help_text="Set to False to hide this word in maps",
    )

    def __str__(self):
        return ("🚩 " if not self.visible else "") + self.text


class WordFrequency(models.Model):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="place_frequencies",
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="word_frequencies",
    )
    frequency = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Word Frequencies"
        constraints = [
            models.UniqueConstraint(
                fields=("word", "place"), name="WordFrequency uniqueness"
            )
        ]

    @classmethod
    def top_words(cls) -> list[tuple[str, int]]:
        query = cls.objects.values("word").annotate(total=Sum("frequency"))
        query = query.order_by("-total")[:10]
        return [(obj["word"], obj["total"]) for obj in query]

    @classmethod
    def create_random(cls, place: Place = None):
        if place is None:
            place = random.choice(Place.objects.all())
        sample, created = cls.objects.get_or_create(
            word=f"WORD{random.randint(0, 20):02d}", place=place
        )
        sample.frequency = F("frequency") + random.randint(1, 10)
        sample.save()

    def __str__(self):
        return f"({self.word} | {self.place})"


    class MapProvider(models.TextChoices):
        TONER_BACKGROUND = "Stamen.TonerBackground", _("Toner Background")
        TONER = "Stamen.Toner", _("Toner")
        TERRAIN = "Stamen.Terrain", _("Terrain")
        WATERCOLOR = "Stamen.Watercolor", _("Watercolor")

class Landscape(TitledModel, LocationModel):
    description = models.TextField(max_length=500, blank=True)

    default = UniqueBooleanField(default=False)

    places = models.ManyToManyField(Place, blank=True)

    reload_time = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=300,
        help_text=_("Reload time (in seconds) for showcase page"),
    )

    provider = models.CharField(
        max_length=100,
        choices=MapProvider.choices,
        default=MapProvider.TONER_BACKGROUND,
        help_text="The map provider to use with leaflet map",
    )

    zoom_initial = models.PositiveSmallIntegerField(default=15)
    zoom_min = models.PositiveSmallIntegerField(default=13)
    zoom_max = models.PositiveSmallIntegerField(default=20)

    @property
    def centroid(self) -> Point:
        if self.places.count() <= 1:
            return self.location
        return self.places.aggregate(centroid=Centroid(Union("location")))["centroid"]

    @property
    def zoom(self):
        return {
            "initial": self.zoom_initial,
            "min": self.zoom_min,
            "max": self.zoom_max,
        }

    def set_centroid(self):
        self.location = self.centroid
        self.save()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="zoom_min <= zoom_initial",
                check=Q(zoom_min__lte=F("zoom_initial")),
            ),
            models.CheckConstraint(
                name="zoom_max >= zoom_initial",
                check=Q(zoom_max__gte=F("zoom_initial")),
            ),
        ]
