import abc
import datetime
import decimal

from django.conf import settings
from django.utils.module_loading import import_string

from data import models

from . import exceptions


class ReadingsConfig(abc.ABC):
    """
    Abstract class to define the interface for a readings' config.
    """

    @abc.abstractmethod
    def create_supply_point(self, **kwargs) -> models.SupplyPoint:
        """
        Create and return a supply point.
        """
        ...

    @abc.abstractmethod
    def create_reading(
        self,
        *,
        value: decimal.Decimal,
        **kwargs,
    ) -> models.Reading: ...

    @abc.abstractmethod
    def ingest_file(self, file_path: str) -> None:
        """
        Ingest a readings' file.

        Raises UnableToIngestReadingsFile if it can't ingest readings for the given file.
        """
        ...

    @abc.abstractmethod
    def get_supply_point(self, identifier: str) -> models.SupplyPoint:
        """
        Get a supply point by its identifier.

        Raises SupplyPointDoesNotExist if the supply point doesn't exist.
        """
        ...

    @abc.abstractmethod
    def get_readings(
        self,
        supply_point: models.SupplyPoint,
        from_dt: datetime.datetime | None = None,
        to_dt: datetime.datetime | None = None,
    ) -> list[dict]:
        """
        Get a supply point's readings as a list of dictionaries.
        """
        ...


def get_config(client_name: str) -> ReadingsConfig:
    """
    Get a ReadingsConfig instance for the given client name.

    Raises UnableToGetReadingsConfig if a config can't be found for the given client.
    """
    try:
        return import_string(settings.READINGS_CONFIG[client_name])()
    except (KeyError, ModuleNotFoundError) as e:
        raise exceptions.UnableToGetReadingsConfig(
            f"Readings config not defined for client {client_name}"
        ) from e
