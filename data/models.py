import decimal

from django.db import models


class DateTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SupplyPoint(DateTimeStampModel):
    class Meta:
        abstract = True

    @classmethod
    def new(cls, **kwargs) -> "SupplyPoint":
        return cls.objects.create(**kwargs)


class Manufacturer(DateTimeStampModel):
    class Meta:
        abstract = True


class Meter(DateTimeStampModel):
    class Meta:
        abstract = True

    @classmethod
    def new(cls, **kwargs) -> "Meter":
        return cls.objects.create(**kwargs)


class Reading(DateTimeStampModel):
    value = models.DecimalField(decimal_places=4, max_digits=16)

    class Meta:
        abstract = True

    @classmethod
    def new(cls, *, value: decimal.Decimal, **kwargs) -> "Reading":
        return cls.objects.create(
            value=value,
            **kwargs,
        )
