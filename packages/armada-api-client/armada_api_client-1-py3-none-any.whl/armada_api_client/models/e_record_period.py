from enum import Enum


class ERecordPeriod(str, Enum):
    ANY = "Any"
    DAY = "Day"
    DELTA = "Delta"
    HOUR = "Hour"
    MINUTE = "Minute"
    SECOND = "Second"

    def __str__(self) -> str:
        return str(self.value)
