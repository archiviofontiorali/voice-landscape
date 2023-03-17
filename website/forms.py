import django.forms
from django.utils.translation import gettext as _

from . import models


class ShareForm(django.forms.ModelForm):
    class Meta:
        model = models.Share
        fields = ["message", "location"]
        labels = {
            "message": _("Esprimi la tua voce"),
        }
        help_texts = {
            "message": _(
                "Scrivi il tuo pensiero qui o usa il tasto microfono per registrare "
                "la tua voce"
            ),
        }
