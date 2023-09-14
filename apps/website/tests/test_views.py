import json
from pathlib import Path

import pytest
from django.shortcuts import reverse
from django.test import Client
from django.utils.text import slugify

from apps.website import models

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def landscape(db, settings):
    with open(FIXTURE_DIR / "landscapes.json", "rt") as fp:
        data = json.load(fp)

    for provider in data["LeafletProvider"]:
        provider.setdefault("slug", slugify(provider["title"]))
        models.LeafletProvider.objects.create(**provider)

    default_provider = models.LeafletProvider.objects.first()

    for landscape in data["Landscape"]:
        landscape.setdefault("provider", default_provider)
        landscape.setdefault("location", settings.DEFAULT_POINT)
        models.Landscape.objects.create(**landscape)

    return models.Landscape.get_default()


@pytest.mark.django_db
def test_404(client):
    response = client.get("/infos")
    assert response.status_code == 404


@pytest.mark.django_db
def test_landscape_cookie(client: Client, landscape):
    response = client.get(url := reverse("website:map"))

    assert response.status_code == 200
    assert response.cookies.get("landscape").value == landscape.slug

    client.cookies.load({"landscape": "prova"})
    response = client.get(url)
    assert response.status_code == 200
    assert response.cookies.get("landscape").value == landscape.slug

    other_landscape = models.Landscape.objects.create(
        title="test",
        slug="test",
        enabled=True,
        provider_id=landscape.provider_id,
        location=landscape.location,
    )

    client.cookies.load({"landscape": "test"})
    response = client.get(url)
    assert response.status_code == 200
    assert response.cookies.get("landscape").value == other_landscape.slug
