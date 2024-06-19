from django.db import models


class UnableToGetReadingsConfig(Exception):
    pass


class UnableToIngestReadingsFile(Exception):
    pass


class SupplyPointDoesNotExist(Exception):
    pass
