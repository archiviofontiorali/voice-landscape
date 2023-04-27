from django.urls import path

from . import views

urlpatterns = [
    path("stt", views.SpeechToText.as_view(), name="stt"),
]
