from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _

from ..website.views import MapTemplateView


class ReloadTemplateView(MapTemplateView):
    def get_reload_from_query(self) -> int | None:
        """Get Reload Time from GET query, convert to int if possible or return None"""
        if (reload := self.request.GET.get("reload")) is None:
            return

        if isinstance(reload, int):
            return max(0, reload)

        if isinstance(reload, str):
            if (reload := reload.strip()).isdigit():
                return int(reload)
            if reload.lower() in ("none", "disable", "false"):
                return 0

        messages.error(self.request, _("Invalid reload value, use default"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("reload", context["landscape"].reload_time)
        if reload := self.get_reload_from_query():
            context["reload"] = reload

        return context


class Showcase(ReloadTemplateView):
    template_name = "showcase/showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("domain", settings.DOMAIN)
        return context
