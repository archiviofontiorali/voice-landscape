import tempfile

import pydub
import pytest
import speech_recognition


@pytest.fixture
def wav_sample() -> str:
    return "tests/data/prova.wav"
    # return "tests/data/OSR_us_000_0010_8k.wav"


def test_speech_recognition(wav_sample, tmp_path):
    sound = pydub.AudioSegment.from_file(wav_sample)
    with open(tmp_path / "prova.wav", "wb") as fp:
        sound.export(fp, format="wav")

    recognizer = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(str(tmp_path / "prova.wav")) as source:
        data = recognizer.record(source)
        text = recognizer.recognize_google(data, language="it-IT")

    assert text == "prova prova prova"
