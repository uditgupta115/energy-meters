import pytest
from django.core.management import call_command
from plugins.clients.carrots import models


@pytest.mark.django_db
def test_should_ingest_readings_file_successfully(carrots_readings_file_path):
    call_command(
        "ingest_readings_file",
        "carrots",
        carrots_readings_file_path,
    )

    assert models.SupplyPoint.objects.count() == 3
    supply_point = models.SupplyPoint.objects.get(identifier="0300111001601606083625")
    assert supply_point.readings.count() == 3
