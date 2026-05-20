import json
from pathlib import Path

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from speech import views


@pytest.fixture
def audio_sample():
    sample_path = Path(__file__).parent / "data" / "sample.ogg"
    media_type = "audio/ogg"
    audio_io = views.read_audio_to_bytes(sample_path, mtype=media_type, codec=None)
    return InMemoryUploadedFile(
        audio_io,
        field_name="audio",
        name="temp.ogg",
        content_type="audio/ogg",
        charset="utf-8",
        size=audio_io.__sizeof__(),
    )


@pytest.mark.django_db
@pytest.mark.slow
def test_stt(client, audio_sample):
    url = reverse("stt")
    response = client.post(url, data={"audio": audio_sample})

    assert response.status_code == 200
    assert json.loads(response.content)["text"].strip().lower() == "test audio"
