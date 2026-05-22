import random
import textwrap
from typing import Optional

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.db.models.aggregates import Union
from django.contrib.gis.db.models.functions import Centroid, Distance
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.db.models import Avg, F, Max, Q, Sum
from django.shortcuts import get_object_or_404, resolve_url
from django.utils import timezone
from django.utils.translation import gettext as _
from django_stubs_ext.db.models import TypedModelMeta

from .fields import UniqueBooleanField
from .tools.geo import Coordinates, coordinates


class OptionalLocationModel(models.Model):
    location = models.PointField(blank=True, null=True)

    x = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    y = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)

    @property
    def latitude(self) -> float:
        return self.location.y if settings.VOICES_ENABLE_GEODJANGO else self.y

    @property
    def longitude(self) -> float:
        return self.location.x if settings.VOICES_ENABLE_GEODJANGO else self.x

    @property
    def coordinates(self) -> Coordinates:
        if settings.VOICES_ENABLE_GEODJANGO:
            return coordinates(self.location)
        else:
            return [float(self.y), float(self.x)]

    def __str__(self):
        lat = f"{self.latitude:7.4f}" if self.latitude is not None else "?"
        lon = f"{self.longitude:7.4f}" if self.longitude is not None else "?"
        return f"{self.__class__.__name__}({lat}, {lon})"

    class Meta(TypedModelMeta):
        abstract = True


class LocationModel(OptionalLocationModel):
    def clean(self):
        if settings.VOICES_ENABLE_GEODJANGO and not self.location:
            raise ValidationError("In GeoDjango mode, location must be filled")

        if not settings.VOICES_ENABLE_GEODJANGO and (self.x is None or self.y is None):
            raise ValidationError("In GeoDjango mode, X and Y must be filled")

    class Meta(TypedModelMeta):
        abstract = True
        constraints = [
            models.CheckConstraint(
                condition=Q(location__isnull=False)
                | (Q(x__isnull=False) & Q(y__isnull=False)),
                name="location_set",
            ),
        ]


class TitledModel(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta(TypedModelMeta):
        abstract = True


class QRModel(TitledModel):
    qr_title = models.CharField(max_length=50, null=True, blank=True)
    qr_subtitle = models.CharField(max_length=100, null=True, blank=True)

    @property
    def qr_url(self) -> str:
        return resolve_url("website:qr-code", place=self.slug)

    class Meta(TypedModelMeta):
        abstract = True


class LeafletProvider(TitledModel):
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=_("The short name to use with provider.js"),
    )
    url = models.URLField(
        max_length=150,
        null=True,
        blank=True,
        help_text=_("The url for a generic leaflet provider"),
    )

    def as_json(self) -> dict:
        return {"url": self.url, "name": self.name}

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(name__isnull=False) | Q(url__isnull=False),
                name="either_name_or_url_not_null",
                violation_error_message=_(
                    _("Either name or url should be set to a valid value")
                ),
            )
        ]


type JSONFrequency = list[str | float]


class Place(LocationModel, QRModel):
    description = models.TextField(max_length=500, blank=True)

    @classmethod
    def get_nearest(cls, location: Point):
        if not settings.VOICES_ENABLE_GEODJANGO:
            raise NotImplementedError("get_nearest implemented only in GeoDjango mode")

        distance = Distance("location", location)
        query = cls.objects.annotate(distance=distance)
        nearest = query.order_by("distance").first()
        if nearest is None:
            raise Exception("Cannot find the nearest place, is at least one set?")
        return nearest

    def get_frequencies(self, min_frequency: int = 2) -> list[JSONFrequency]:
        """Return a list of [word, frequency] with the latest normalized"""
        filters = dict(frequency__gte=min_frequency, word__visible=True)
        frequencies = self.word_frequencies.filter(**filters)  # type: ignore
        frequencies = frequencies.order_by("-frequency")[:50]
        max_ = frequencies.aggregate(Max("frequency"))["frequency__max"]
        return [[wf.word.text, wf.frequency / max_] for wf in frequencies]

    def as_json(self):
        return {"coordinates": self.coordinates, "frequencies": self.get_frequencies()}

    def get_absolute_url(self):
        return resolve_url("website:share", place=self.slug)

    def __str__(self):
        return f"{self.__class__.__name__}<{self.title}>"

    class Meta(TypedModelMeta):
        abstract = False


class Word(models.Model):
    text = models.CharField(max_length=100, unique=True)
    visible = models.BooleanField(
        default=True,
        help_text="Set to False to hide this word in maps",
    )

    def __str__(self):
        return ("🚩 " if not self.visible else "") + self.text


class Share(LocationModel):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField(max_length=500)
    landscape = models.ForeignKey("Landscape", on_delete=models.CASCADE)

    place = models.ForeignKey(
        Place,
        related_name="shares",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    words = models.ManyToManyField(Word, related_name="shares", blank=True)

    def __str__(self):
        message = textwrap.shorten(self.message, width=20, placeholder="...")
        return f"{super().__str__()} [{message}]"


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
        ordering = ("-frequency",)
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
    def create_random(cls, place: Optional[Place] = None):
        if place is None:
            place = random.choice(Place.objects.all())
        sample, _created = cls.objects.get_or_create(
            word=f"WORD{random.randint(0, 20):02d}", place=place
        )
        sample.frequency = F("frequency") + random.randint(1, 10)
        sample.save()

    def __str__(self):
        return f"({self.word} | {self.place})"


class Logo(models.Model):
    name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(
        upload_to="logos/", height_field="height", width_field="width"
    )
    width = models.PositiveSmallIntegerField(null=True, blank=True, editable=False)
    height = models.PositiveSmallIntegerField(null=True, blank=True, editable=False)

    @property
    def url(self):
        return self.image.url

    def __str__(self):
        return self.name if self.name else super().__str__()


class Landscape(TitledModel, LocationModel):
    description = models.TextField(max_length=500, blank=True)
    domain = models.URLField(
        blank=True,
        help_text=_("Domain in showcase page. Leave blank to use the one in .env"),
    )

    default = UniqueBooleanField(default=False)
    enabled = models.BooleanField(
        default=True,
        help_text=_("Set to False to hide it in views, unless is chosen as default"),
    )

    places = models.ManyToManyField(Place, blank=True)

    reload_time = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=300,
        help_text=_("Reload time (in seconds) for showcase page"),
    )

    provider = models.ForeignKey(
        LeafletProvider,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text="The map provider to use with leaflet map",
    )

    zoom_initial = models.PositiveSmallIntegerField(default=15)
    zoom_min = models.PositiveSmallIntegerField(default=13)
    zoom_max = models.PositiveSmallIntegerField(default=20)

    logo_event = models.ForeignKey(
        Logo,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None,
        related_name="+",
    )
    logo_organizer = models.ForeignKey(
        Logo,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None,
        related_name="+",
    )
    logo_partners = models.ManyToManyField(to=Logo, related_name="+", blank=True)

    @property
    def centroid(self) -> Coordinates:
        if self.places.count() <= 1:
            return self.coordinates

        if settings.VOICES_ENABLE_GEODJANGO:
            p = self.places.aggregate(centroid=Centroid(Union("location")))["centroid"]
            return coordinates(p)

        return [
            float(self.places.aggregate(mean=Avg("y"))["mean"]),
            float(self.places.aggregate(mean=Avg("x"))["mean"]),
        ]

    @property
    def zoom(self):
        return {
            "initial": self.zoom_initial,
            "min": self.zoom_min,
            "max": self.zoom_max,
        }

    def set_centroid(self):
        if settings.VOICES_ENABLE_GEODJANGO:
            self.location = Point(*self.centroid)
        else:
            self.y, self.x = self.centroid

        self.save()

    @classmethod
    def get_default(cls) -> "Landscape":
        return get_object_or_404(cls, default=True)

    class VisibleLandscapeManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(Q(enabled=True) | Q(default=True))

        def get_default(self):
            return self.get(default=True)

    objects = models.Manager()
    visible_objects = VisibleLandscapeManager()

    class Meta:  # type: ignore
        constraints = [
            models.CheckConstraint(
                name="zoom_min <= zoom_initial",
                condition=Q(zoom_min__lte=F("zoom_initial")),
            ),
            models.CheckConstraint(
                name="zoom_max >= zoom_initial",
                condition=Q(zoom_max__gte=F("zoom_initial")),
            ),
        ]
