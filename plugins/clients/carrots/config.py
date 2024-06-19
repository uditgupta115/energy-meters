import datetime
import decimal
import json

from domain.readings import config

from . import models
from .enums import ReadingMethodType


class ReadingsConfig(config.ReadingsConfig):
    def create_supply_point(self, **kwargs) -> models.SupplyPoint:
        return models.SupplyPoint.new(
            identifier=kwargs["identifier"],
        )

    def create_reading(
        self,
        *,
        value: decimal.Decimal,
        **kwargs,
    ) -> models.Reading:
        return models.Reading.objects.get_or_create(
            value=value,
            read_at=kwargs["read_at"],
            supply_point=kwargs["supply_point"],
            meter=kwargs['meter'],
            time_code=kwargs.get('time_code'),
            reading_method=kwargs.get('reading_method'),
        )

    def ingest_file(self, file_path: str, **kwargs) -> None:

        with open(file_path, 'r+', encoding='utf-8') as f:
            data = f.readlines()

        for each_row in data:
            row_data = each_row.strip().split('|')
            group = row_data[0]
            if group == '020':
                # create supplypoints
                supply_point, created = models.SupplyPoint.objects.get_or_create(
                    identifier=row_data[1]
                )
            elif group == '022':
                serial_number = row_data[1]
                manufacturer_name = row_data[2]
                reading_type = row_data[3]
                manufacturer, created = models.Manufacturer.objects.get_or_create(
                    name=manufacturer_name
                )
                print(f'manufacturer --> {manufacturer}', created)
                meter, created = models.Meter.objects.get_or_create(
                    supply_point=supply_point,
                    manufacturer=manufacturer,
                    serial_number=serial_number,
                    reading_type=reading_type,
                )
                print(f'meter --> {meter}', created)
            elif group in ('024', '026'):
                # readings group
                reading = None
                if group == '024' and reading_type == '01':
                    reading_date = datetime.datetime.strptime(
                        row_data[1], '%Y%m%d'
                    )
                    reading, created = self.create_reading(
                        supply_point=supply_point,
                        meter=meter,
                        value=decimal.Decimal(str(row_data[3])),
                        read_at=reading_date,
                        time_code=row_data[2],
                        reading_method=ReadingMethodType.T.name
                    )
                elif group == '026' and reading_type == '02':
                    reading_date = datetime.datetime.strptime(
                        row_data[1], '%Y%m%d%H%M%S'
                    )
                    reading, created = self.create_reading(
                        supply_point=supply_point,
                        meter=meter,
                        value=decimal.Decimal(str(row_data[2])),
                        read_at=reading_date,
                        reading_method=row_data[3].upper()
                    )

                print(f'reading --> {reading}', created)

    def get_supply_point(self, identifier: str) -> models.SupplyPoint:
        return models.SupplyPoint.objects.get(identifier=identifier)

    def get_readings(
        self,
        supply_point: models.SupplyPoint,
        from_dt: datetime.datetime | None = None,
        to_dt: datetime.datetime | None = None,
    ) -> list[dict]:
        readings = supply_point.readings.filter(is_deleted=False)
        if from_dt:
            readings = readings.filter(read_at__gte=from_dt)
        if to_dt:
            readings = readings.filter(read_at__lt=to_dt)
        return [
            {
                "value": str(reading.value),
                "read_at": reading.read_at.isoformat(),
            }
            for reading in readings
        ]
