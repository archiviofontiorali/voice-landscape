import django.forms
from django.contrib.gis.forms import CharField, DecimalField, Textarea
from django.utils.translation import gettext as _


class ShareForm(django.forms.Form):
    message = CharField(
        label=_("Esprimi la tua voce"),
        help_text=_(
            "Scrivi il tuo pensiero qui o usa il tasto microfono per "
            "registrare la tua voce"
        ),
        widget=Textarea,
        max_length=500,  # TODO: find a way to use same value in form and model
    )

    latitude = DecimalField(label=_("Latitudine"))
    longitude = DecimalField(label=_("Longitudine"))
