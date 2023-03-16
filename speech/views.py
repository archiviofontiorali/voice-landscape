import io

import pydub
import speech_recognition
from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.views import View


class SpeechToText(View):
    recognizer = speech_recognition.Recognizer()

    def post(self, request: HttpRequest):
        if not (data := request.FILES.get("audio")):
            raise ValidationError

        audio = io.BytesIO()
        sound = pydub.AudioSegment.from_file(data.file)
        sound.export(audio, format="wav")

        # TODO: enable italian language recognition. Follow this link:
        #  https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst#installing-other-languages

        with speech_recognition.AudioFile(audio) as source:
            data = self.recognizer.record(source)
            text = self.recognizer.recognize_sphinx(data)
        return JsonResponse({"text": text})
