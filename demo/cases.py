import tempfile

import pydub
import spacy
import spacy.symbols
import speech_recognition
from loguru import logger
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.templating import Jinja2Templates

from .constants import SHOWCASE_RELOAD_TIME
from .geo import Coordinates, find_nearest_place, prepare_map_frequencies
from .repos import FrequencyRepo

# TODO: create presenters
templates = Jinja2Templates(directory="templates")


class HomePage:
    @staticmethod
    async def execute(request):
        context = {"request": request}
        return templates.TemplateResponse("index.html", context)


class LeafletMapPage:
    def __init__(self, frequency_repo: FrequencyRepo):
        self._frequency_repo = frequency_repo

    async def execute(self, request):
        places = prepare_map_frequencies(self._frequency_repo)
        context = {
            "places": places,
            "request": request,
        }
        return templates.TemplateResponse("map.html", context)


class ShowcasePage:
    def __init__(self, frequency_repo: FrequencyRepo):
        self._frequency_repo = frequency_repo

    async def execute(self, request):
        places = prepare_map_frequencies(self._frequency_repo)
        context = {
            "reload": SHOWCASE_RELOAD_TIME,
            "places": places,
            "request": request,
        }
        return templates.TemplateResponse("showcase.html", context)


class SharePage:
    def __init__(self, frequency_repo: FrequencyRepo):
        self._frequency_repo = frequency_repo
        self._nlp = spacy.load("it_core_news_sm")

    async def execute(self, target: Coordinates, text: str, request):
        if request.method == "POST":
            logger.debug(f"Receiving text from {target}: {text}")
            nearest_place, _ = find_nearest_place(target, self._frequency_repo.places)

            doc = self._nlp(text)
            for token in doc:
                if token.pos in (
                    spacy.symbols.ADV,
                    spacy.symbols.NOUN,
                    spacy.symbols.VERB,
                    spacy.symbols.ADJ,
                ):
                    self._frequency_repo.update_frequency(nearest_place, token.lemma_)

        context = {"request": request}
        return templates.TemplateResponse("share.html", context)


class SpeechToText:
    def __init__(self):
        self._recognizer = speech_recognition.Recognizer()

    async def execute(self, request, audio: tempfile.SpooledTemporaryFile):
        sound = pydub.AudioSegment.from_file(audio)
        raw = tempfile.NamedTemporaryFile(suffix=".wav")
        sound.export(raw, format="wav")

        with speech_recognition.AudioFile(raw.name) as source:
            data = self._recognizer.record(source)
            text = self._recognizer.recognize_google(data, language="it-IT")
        return JSONResponse(text)


class Ping:
    def __init__(self):
        self._response = "Pong!"

    async def execute(self, request):
        logger.debug(self._response)
        return PlainTextResponse(self._response)
