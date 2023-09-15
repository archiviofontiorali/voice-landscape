from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "website"
urlpatterns = [
    path("", views.Map.as_view()),
    path("map/", views.Map.as_view(), name="map"),
    path("share/", views.Share.as_view(), name="share"),
]
