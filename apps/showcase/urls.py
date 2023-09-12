from django.urls import path, reverse
from django.views.generic import RedirectView

from . import views

app_name = "showcase"
urlpatterns = [
    path("", RedirectView.as_view(url="view")),
    path("view/", views.ShowcasePage.as_view(), name="view"),
    path("view/<slug:slug>", views.ShowcasePage.as_view(), name="view"),
]
