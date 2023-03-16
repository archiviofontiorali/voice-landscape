import tempfile

import pydub
import spacy
import spacy.symbols
import speech_recognition
from loguru import logger

from .constants import CENTER_COORDINATES, SHOWCASE_RELOAD_TIME
from .repos import FrequencyRepo
from .system.types import Case


class TemplatePage(Case):
    def __init__(self, template: str):
        self.template = template

    async def execute(self, request, presenter):
        return presenter.render(self.template, {"request": request})


class LeafletMapPage(Case):
    def __init__(self, template: str, frequency_repo: FrequencyRepo):
        self.template = template
        self._frequency_repo = frequency_repo

    async def execute(self, request, presenter):
        places = await self._frequency_repo.prepare_map_frequencies()
        context = {
            "center": CENTER_COORDINATES,
            "places": places,
            "request": request,
        }
        return presenter.render(self.template, context)


class ShowcasePage(Case):
    def __init__(self, template: str, frequency_repo: FrequencyRepo):
        self.template = template
        self._frequency_repo = frequency_repo

    async def execute(self, request, presenter):
        places = await self._frequency_repo.prepare_map_frequencies()
        stats = await self._frequency_repo.statistics()
        context = {
            "center": CENTER_COORDINATES,
            "reload": SHOWCASE_RELOAD_TIME,
            "places": places,
            "stats": stats,
            "request": request,
        }
        return presenter.render(self.template, context)


class SharePage(Case):
    def __init__(self, template: str, frequency_repo: FrequencyRepo):
        self.template = template
        self._frequency_repo = frequency_repo
        self._nlp = spacy.load("it_core_news_sm")

    @staticmethod
    def find_nearest_place(
        target: Coordinates, places: Iterable[Coordinates]
    ) -> Tuple[Coordinates, float]:
        near, distance = None, math.inf
        for place in places:
            new_distance = geopy.distance.geodesic(target, place).m
            if new_distance < distance:
                near, distance = place, new_distance
        return near, distance

    async def execute(self, request, presenter):
        if request.method == "POST":
            data = await request.form()

            coordinates = (
                float(data.get("loc-x", None)),
                float(data.get("loc-y", None)),
            )
            text = data.get("text", None)

            logger.debug(f"Receiving text from {coordinates}: {text}")
            nearest, _ = self.find_nearest_place(
                coordinates, self._frequency_repo.places
            )

            doc = self._nlp(text)
            for token in doc:
                if token.pos in (
                    spacy.symbols.ADV,
                    spacy.symbols.NOUN,
                    spacy.symbols.VERB,
                    spacy.symbols.ADJ,
                ):
                    await self._frequency_repo.update_frequency(nearest, token.lemma_)

        context = {"request": request}
        return presenter.render(self.template, context)


class SpeechToText(Case):
    def __init__(self):
        self._recognizer = speech_recognition.Recognizer()

    async def execute(self, request, presenter):
        # TODO: check data.content-type
        audio = (await request.form()).get("audio", None)
        sound = pydub.AudioSegment.from_file(audio.file if audio else None)
        raw = tempfile.NamedTemporaryFile(suffix=".wav")
        sound.export(raw, format="wav")

        with speech_recognition.AudioFile(raw.name) as source:
            data = self._recognizer.record(source)
            text = self._recognizer.recognize_google(data, language="it-IT")
        return presenter.json(text)
