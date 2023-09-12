from django.conf import settings

from ..website.views import MapPage


class ReloadTemplateView(MapPage):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Reload time is set from landscape unless an int or keyword is passed in query
        context.setdefault("reload", context["landscape"].reload_time)
        if (reload := self.request.GET.get("reload")) and isinstance(reload, str):
            if (reload := reload.strip()).isdigit():
                context["reload"] = max(0, int(reload))
            if reload.lower() in ("none", "disable", "false"):
                context["reload"] = 0

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
