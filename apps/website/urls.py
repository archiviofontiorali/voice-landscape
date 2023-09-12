from django.urls import path
from django.views.generic import RedirectView, TemplateView

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # path("", RedirectView.as_view(url="map/")),
    path("map/", views.MapPage.as_view(), name="map"),
    path("map/<slug:slug>", views.MapPage.as_view(), name="map"),
    path("share/", views.SharePage.as_view(), name="share"),
    path("share/<slug:slug>", views.SharePage.as_view(), name="share"),
]
