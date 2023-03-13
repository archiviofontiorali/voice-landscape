from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("map", views.MapPage.as_view(), name="map"),
    path("share", views.SharePage.as_view(), name="share"),
    path("showcase", views.ShowcasePage.as_view(), name="showcase"),
]
