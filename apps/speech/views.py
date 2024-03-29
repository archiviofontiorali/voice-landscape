import datetime as dt
import io
import pathlib
import re

import pydub
import speech_recognition
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext as _
from django.views import View
from loguru import logger

from .errors import SpeechRecognitionError, UnsupportedSpeechRecognitionError
from .forms import UploadAudioForm

DATA_SPEECH_ROOT: pathlib.Path = settings.DATA_ROOT / "speech"
DATA_SPEECH_ROOT.mkdir(exist_ok=True, parents=True)

MEDIA_TYPE_REGEX = re.compile(r"audio/(?P<format>\w+)(?:;\s?codecs=(?P<codecs>\w+))?")


def timestamp(t: dt.datetime = None):
    if t is None:
        t = dt.datetime.now()
    return t.isoformat(timespec="seconds")


def read_audio_to_bytes(path, mtype, codec) -> io.BytesIO:
    sound = pydub.AudioSegment.from_file(path, format=mtype, codec=codec)
    if settings.SPEECH_RECOGNITION_DEBUG:
        path = DATA_SPEECH_ROOT / f"sample_{timestamp()}.{mtype}"
        sound.export(path, format=mtype, codec=codec)

    sound.export(audio := io.BytesIO(), format="wav")

    logger.debug(
        f"[pydub] channels: {sound.channels}, frame_rate: {sound.frame_rate}, "
        f"duration: {sound.duration_seconds:.2f}"
    )

    return audio


class JsonErrorResponse(JsonResponse):
    def __init__(self, message, status: int = 400, **kwargs):
        response = {"message": message, "status_code": status}
        super().__init__(response, status=status, **kwargs)


class SpeechToText(View):
    recognizer = speech_recognition.Recognizer()

    def transcribe_with_whisper(self, data: speech_recognition.audio.AudioData):
        return self.recognizer.recognize_whisper(
            data,
            language=settings.WHISPER_LANGUAGE,
            model=settings.WHISPER_MODEL,
        )

    def transcribe_with_google(self, data: speech_recognition.audio.AudioData):
        return self.recognizer.recognize_google(data, language="it-IT")

    def transcribe_audio(self, audio: io.BytesIO) -> str:
        with speech_recognition.AudioFile(audio) as source:
            data = self.recognizer.record(source)

        match settings.SPEECH_RECOGNITION_SERVICE.lower():
            case "whisper":
                return self.transcribe_with_whisper(data)
            case "google":
                return self.transcribe_with_google(data)
            case _:
                raise UnsupportedSpeechRecognitionError

    def post(self, request: HttpRequest):
        form = UploadAudioForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonErrorResponse("Invalid audio request", status=400)

        mtype, codec = MEDIA_TYPE_REGEX.match(form.cleaned_data["media_type"]).groups()
        audio = read_audio_to_bytes(request.FILES["audio"], mtype=mtype, codec=codec)

        try:
            text = self.transcribe_audio(audio)
        except speech_recognition.exceptions.UnknownValueError:
            return JsonErrorResponse(_("Audio non comprensibile, riprova"), status=400)
        except SpeechRecognitionError as err:
            return JsonErrorResponse(err.message, status=500)

        logger.debug(f"[speech_recognition] transcription: {text}")
        return JsonResponse({"text": text})
