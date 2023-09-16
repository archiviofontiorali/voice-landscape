from django.urls import path, register_converter
from django.utils import timezone

from . import views


class DateTimeConverter:
    regex = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"

    @staticmethod
    def to_python(value):
        time = timezone.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        return timezone.make_aware(time)

    @staticmethod
    def to_url(value):
        return value


register_converter(DateTimeConverter, "datetime")

app_name = "website"
urlpatterns = [
    path("", views.Map.as_view()),
    path("map/", views.Map.as_view(), name="map"),
    path("share/", views.Share.as_view(), name="share"),
    path("history/", views.HistoryMap.as_view(), name="history"),
    path("history/<datetime:timestamp>/", views.HistoryMap.as_view(), name="history"),
]
