from django.views import generic


class HomePage(generic.TemplateView):
    template_name = "home.html"


class SharePage(generic.TemplateView):
    template_name = "share.html"


class MapPage(generic.TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.setdefault("places", [])
        return context


class ShowcasePage(generic.TemplateView):
    template_name = "showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.setdefault("places", [])
        return context
