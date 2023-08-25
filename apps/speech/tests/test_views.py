import json

import pytest
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import reverse

from apps.speech import views


@pytest.fixture
def audio_sample():
    audio_io = views.read_audio_to_bytes(
        settings.BASE_DIR / "tests" / "data" / "sample.ogg"
    )
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
