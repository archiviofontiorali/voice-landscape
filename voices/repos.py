from abc import ABC
from typing import Iterable, List

import spacy
import spacy.symbols

from .constants import PLACES

Coordinates = tuple[float, float]

# TODO: with bisect module and custom structure it's possible to improve performance


class FrequencyRepo(ABC):
    places: Iterable[Coordinates]

    def update_frequency(self, place: Coordinates, key: str):
        pass

    def fetch_frequency_table(self, place: Coordinates) -> dict:
        pass

    # async def prepare_map_frequencies(self):
    #     pass

    async def statistics(self):
        pass


class FrequencySQLRepo(FrequencyRepo):
    def __init__(self, db):
        self._db = db
        self._table = "frequencies"
        self._keys = ", ".join(
            [
                "latitude FLOAT8 NOT NULL",
                "longitude FLOAT8 NOT NULL",
                "word TEXT NOT NULL",
                "frequency INT DEFAULT 1",
                "PRIMARY KEY(latitude, longitude, word)",
            ]
        )

        self._coordinates = list(PLACES.keys())

    async def init_db(self):
        await self._db.create_table(self._table, self._keys)

    @property
    def places(self) -> Iterable[Coordinates]:
        return self._coordinates

    async def update_frequency(self, place: Coordinates, key: str):
        values = dict(latitude=place[0], longitude=place[1], word=key)
        query = (
            f"INSERT INTO {self._table}(latitude, longitude, word) "
            "VALUES (:latitude, :longitude, :word) "
            "ON CONFLICT (latitude, longitude, word) "
            "DO UPDATE SET frequency = frequencies.frequency + 1"
        )
        await self._db.execute(query, **values)

    async def fetch_frequency_table(self, place: Coordinates) -> List[tuple]:
        values = dict(latitude=place[0], longitude=place[1])
        query = (
            f"SELECT word, frequency FROM {self._table} "
            "WHERE latitude=:latitude AND longitude=:longitude"
        )
        return await self._db.fetch_all(query, **values)

    async def statistics(self):
        query = (
            f"SELECT word, sum(frequency) AS frequency FROM {self._table} "
            "GROUP BY word ORDER BY frequency DESC LIMIT :top"
        )
        top_words = await self._db.fetch_all(query, top=10)
        return {"top_words": [(row[0], row[1]) for row in top_words]}


class NLP:
    VALID_TOKENS = (
        spacy.symbols.ADV,
        spacy.symbols.NOUN,
        spacy.symbols.VERB,
        spacy.symbols.ADJ,
    )

    def __init__(self):
        self._nlp = spacy.load("it_core_news_sm")

    def preprocess(self, message: str):
        # TODO: sanitize content for example with `bleach`
        tokens = (
            token.lemma_
            for token in self._nlp(message)
            if token.pos in self.VALID_TOKENS
        )
        return list(tokens)
