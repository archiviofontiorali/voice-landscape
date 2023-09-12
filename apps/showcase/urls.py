from django.urls import path, reverse
from django.views.generic import RedirectView

from . import views

app_name = "showcase"
urlpatterns = [
    path("", views.ShowcasePage.as_view(), name="view"),
    path("<slug:slug>", views.ShowcasePage.as_view(), name="view"),
]
