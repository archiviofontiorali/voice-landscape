from abc import ABC

from django.utils.translation import gettext as _


class SpeechRecognitionError(ABC, Exception):
    message: str


class UnsupportedSpeechRecognitionError(SpeechRecognitionError):
    message = _("Unsupported speech recognition system")
