from django.urls import path

from . import views

urlpatterns = [
    path("", views.ShowcasePage.as_view(), name="showcase"),
    path("<slug:slug>", views.ShowcasePage.as_view(), name="showcase"),
]
