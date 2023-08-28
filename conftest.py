import pytest
from django.db import connection


@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        with connection.cursor() as c:
            c.execute("SELECT InitSpatialMetaData(1);")
