from django.views import generic

from . import models


class HomePage(generic.TemplateView):
    template_name = "home.html"


class SharePage(generic.TemplateView):
    template_name = "share.html"


class MapPage(generic.TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        landscape = models.Landscape.objects.first()
        coords = [landscape.center.y, landscape.center.x] if landscape else [0, 0]
        context["center"] = coords

        context.setdefault("places", [])

        return context


class ShowcasePage(generic.TemplateView):
    template_name = "showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.setdefault("places", [])
        return context
