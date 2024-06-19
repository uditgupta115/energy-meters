from data.enums import BaseEnum


class Mapping:
    INTERVAL = '01'
    ACCUMULATION = '02'


class MeterReadingType(BaseEnum):
    Mapping.INTERVAL = 'Interval'
    Mapping.ACCUMULATION = 'Accumulation'


class ReadingMethodType(BaseEnum):
    N = 'Not viewed by an Agent'
    P = 'Viewed by an Agent'
    S = 'Automatically collected via network'
    T = 'Time based Reading'
