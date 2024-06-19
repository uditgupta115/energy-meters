from django.core.management import call_command
from plugins.clients.potatoes import models


def test_should_ingest_readings_file_successfully(potatoes_readings_file_path):
    call_command(
        "ingest_readings_file",
        "potatoes",
        potatoes_readings_file_path,
    )

    assert models.SupplyPoint.objects.count() == 1
    supply_point = models.SupplyPoint.objects.get(identifier="120000003100")
    assert supply_point.readings.count() == 4
