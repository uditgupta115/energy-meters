from django.core.management import base
from domain.readings import config as readings_config
from domain.readings import exceptions as readings_exceptions


class Command(base.BaseCommand):
    """
    Ingest a readings file for a given client.
    """

    def add_arguments(self, parser: base.CommandParser) -> None:
        parser.add_argument("client_name", type=str)
        parser.add_argument("file_path", type=str)

    def handle(self, client_name: str, file_path: str, **options) -> None:
        try:
            config = readings_config.get_config(client_name)
            config.ingest_file(file_path)
        except (
            readings_exceptions.UnableToGetReadingsConfig,
            readings_exceptions.UnableToIngestReadingsFile,
        ) as e:
            raise base.CommandError(f"Unable to parse readings: {str(e)}") from e
