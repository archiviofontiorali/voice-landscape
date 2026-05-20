"""
URL configuration for voices project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


def template_view(template_name: str, **kwargs):
    return TemplateView.as_view(template_name=template_name, **kwargs)


urlpatterns = [
    path("", include("website.urls", namespace="website")),
    # path("showcase/", include("apps.showcase.urls", namespace="showcase")),
    # path("api/", include("apps.api.urls")),
    # path("api/speech/", include("apps.speech.urls")),
    # Static pages
    path("info/", template_view("info.html"), name="info"),
    path("privacy/", template_view("privacy.html"), name="privacy"),
    path("robots.txt", template_view("robots.txt", content_type="text/plain")),
    # Admin
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
