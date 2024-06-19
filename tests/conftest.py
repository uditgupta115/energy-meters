import os

import pytest
from django.conf import settings


@pytest.fixture(scope="class")
def potatoes_readings_file_path():
    return os.path.join(
        settings.BASE_DIR,
        "tests/fixtures/potatoes/readings.json",
    )


@pytest.fixture(scope="class")
def carrots_readings_file_path():
    return os.path.join(
        settings.BASE_DIR,
        "tests/fixtures/carrots/readings.txt",
    )


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass
