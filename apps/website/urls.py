from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("map", views.LandscapeMap.as_view(), name="map"),
    path("map/<slug:slug>", views.LandscapeMap.as_view(), name="map"),
    path("share", views.SharePage.as_view(), name="share"),
    path("showcase", views.LandscapeShowcase.as_view(), name="showcase"),
    path("showcase/<slug:slug>", views.LandscapeShowcase.as_view(), name="showcase"),
    path("privacy", views.PrivacyPage.as_view(), name="privacy"),
    path("robots.txt", views.robots_txt, name="robots"),
]
