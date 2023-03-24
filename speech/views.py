import datetime as dt
import io
import pathlib

import pydub
import speech_recognition
from django import forms
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext as _
from django.views import View
from loguru import logger

DATA_SPEECH_ROOT: pathlib.Path = settings.DATA_ROOT / "speech"
DATA_SPEECH_ROOT.mkdir(exist_ok=True, parents=True)


def timestamp(t: dt.datetime = None):
    if t is None:
        t = dt.datetime.now()
    return t.isoformat(timespec="seconds")


class JsonErrorResponse(JsonResponse):
    def __init__(self, message, status: int = 400, **kwargs):
        response = {"message": message, "status_code": status}
        super().__init__(response, status=status, **kwargs)


class UploadAudioForm(forms.Form):
    audio = forms.FileField()


class SpeechToText(View):
    recognizer = speech_recognition.Recognizer()

    def post(self, request: HttpRequest):
        form = UploadAudioForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonErrorResponse("Invalid audio request", status=400)

        sound = pydub.AudioSegment.from_file(request.FILES["audio"])
        if settings.SPEECH_RECOGNITION_DEBUG:
            sound.export(DATA_SPEECH_ROOT / f"sample_{timestamp()}.wav", format="wav")
        sound.export(audio := io.BytesIO(), format="wav")

        logger.debug(
            f"[pydub] channels: {sound.channels}, frame_rate: {sound.frame_rate}, "
            f"duration: {sound.duration_seconds:.2f}"
        )

        with speech_recognition.AudioFile(audio) as source:
            data = self.recognizer.record(source)
        try:
            text = self.recognizer.recognize_google(data, language="it-IT")
        except speech_recognition.exceptions.UnknownValueError:
            return JsonErrorResponse(_("Audio non comprensibile, riprova"), status=400)

        logger.debug(f"[speech_recognition] transcription: {text}")
        return JsonResponse({"text": text})
