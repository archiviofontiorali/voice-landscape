from django.urls import path
from django.views.generic import RedirectView, TemplateView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="map/")),
    path("map/", views.MapPage.as_view(), name="map"),
    path("map/<slug:slug>", views.MapPage.as_view()),
    path("share/", views.SharePage.as_view(), name="share"),
    path("share/<slug:slug>", views.SharePage.as_view()),
]
