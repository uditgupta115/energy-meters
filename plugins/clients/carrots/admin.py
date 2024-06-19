from django.contrib import admin

from . import models


@admin.register(models.SupplyPoint)
class SupplyPointAdmin(admin.ModelAdmin):
    list_display = ["identifier"]


@admin.register(models.Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(models.Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ("serial_number", 'is_active', 'reading_type',)


@admin.register(models.Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "read_at",
        'time_code',
        "value",
        'is_deleted',
        'reading_method'
    ]
