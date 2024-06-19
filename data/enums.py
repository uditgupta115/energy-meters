from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def choices(cls):
        return ((tag.name, tag.value) for tag in cls)
