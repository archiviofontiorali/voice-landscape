"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

urlpatterns = [
    # apps
    path("", include("apps.website.urls", namespace="website")),
    path("showcase/", include("apps.showcase.urls", namespace="showcase")),
    path("api/", include("apps.api.urls")),
    path("api/speech/", include("apps.speech.urls")),
    # Static pages
    path("info/", TemplateView.as_view(template_name="info.html"), name="info"),
    path(
        "privacy/", TemplateView.as_view(template_name="privacy.html"), name="privacy"
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    # Third party libraries
    path("admin/", admin.site.urls),
    path("qr_code/", include("qr_code.urls", namespace="qr_code")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
