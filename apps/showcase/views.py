from django.conf import settings
from django.views.generic import TemplateView

from ..website.views import MapPage


class ReloadTemplateView(MapPage):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reload_time = self.request.GET.get("reload", context["landscape"].reload_time)
        context.setdefault("reload", reload_time)
        return context


class ShowcasePage(ReloadTemplateView):
    template_name = "showcase/showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("domain", settings.DOMAIN)
        context.setdefault("qr_url", f"https://{settings.DOMAIN}")
        return context


class ShowcasePageImage(TemplateView):
    pass
