from django.views import generic

from . import voices


class HomePage(generic.TemplateView):
    template_name = "home.html"


class SharePage(generic.TemplateView):
    template_name = "share.html"


class MapPage(generic.TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context.setdefault("places", voices.extrapolate_place_word_frequencies())
        context.setdefault("center", voices.calculate_places_centroid())

        return context


class ShowcasePage(generic.TemplateView):
    template_name = "showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context.setdefault("places", voices.extrapolate_place_word_frequencies())
        context.setdefault("center", voices.calculate_places_centroid())

        return context
