from enum import Enum


class EAggregate(str, Enum):
    COUNT = "count"
    FIRST = "first"
    LAST = "last"
    MAX = "max"
    MEAN = "mean"
    MEDIAN = "median"
    MIN = "min"
    SPREAD = "spread"
    SUM = "sum"

    def __str__(self) -> str:
        return str(self.value)
