from django.urls import path

from . import views

app_name = "showcase"
urlpatterns = [
    path("", views.Showcase.as_view(), name="view"),
]
