from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from data import models as base_models
from plugins.clients.carrots.enums import MeterReadingType, ReadingMethodType


def validate_time_code(value):
    if value not in (range(1, 49)):
        raise ValidationError(
            _("%(value)s is not an given range should be 1 to 48"),
            params={"value": value},
        )


class SupplyPoint(base_models.SupplyPoint):
    identifier = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.identifier


class Manufacturer(base_models.Manufacturer):
    name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.name


class Meter(base_models.Meter):
    supply_point = models.ForeignKey(
        SupplyPoint,
        on_delete=models.CASCADE,
        related_name="meters",
    )
    serial_number = models.CharField(
        max_length=10,
        null=False,
        blank=False,
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="meters",
    )
    is_active = models.BooleanField(default=True)
    reading_type = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        choices=MeterReadingType.choices()
    )

    def __str__(self):
        return self.serial_number


class Reading(base_models.Reading):
    supply_point = models.ForeignKey(
        SupplyPoint,
        on_delete=models.CASCADE,
        related_name="readings",
    )
    meter = models.ForeignKey(
        Meter,
        on_delete=models.CASCADE,
        related_name="readings",
    )
    read_at = models.DateTimeField(null=False)
    is_deleted = models.BooleanField(default=False)
    reading_method = models.CharField(
        max_length=4, null=True, blank=True,
        choices=ReadingMethodType.choices()
    )
    time_code = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        # validators=[validate_time_code]
    )

    def __str__(self):
        return f'{self.value}'
