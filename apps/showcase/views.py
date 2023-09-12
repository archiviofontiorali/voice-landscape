from django.conf import settings

from ..website.views import MapPage


class ShowcasePage(MapPage):
    template_name = "showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reload_time = self.request.GET.get("reload", context["landscape"].reload_time)
        context.setdefault("reload", reload_time)
        context.setdefault("domain", settings.DOMAIN)
        context.setdefault("qr_url", f"https://{settings.DOMAIN}")
        return context
