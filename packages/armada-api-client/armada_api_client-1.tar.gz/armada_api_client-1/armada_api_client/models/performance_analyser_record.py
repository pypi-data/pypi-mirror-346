import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="PerformanceAnalyserRecord")


@_attrs_define
class PerformanceAnalyserRecord:
    """
    Attributes:
        id (int):
        analyser_id (int):
        average (float):
        min_ (float):
        max_ (float):
        date (datetime.datetime):
        period_in_second (int):
    """

    id: int
    analyser_id: int
    average: float
    min_: float
    max_: float
    date: datetime.datetime
    period_in_second: int

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        analyser_id = self.analyser_id

        average = self.average

        min_ = self.min_

        max_ = self.max_

        date = self.date.isoformat()

        period_in_second = self.period_in_second

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "analyserId": analyser_id,
                "average": average,
                "min": min_,
                "max": max_,
                "date": date,
                "periodInSecond": period_in_second,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        analyser_id = d.pop("analyserId")

        average = d.pop("average")

        min_ = d.pop("min")

        max_ = d.pop("max")

        date = isoparse(d.pop("date"))

        period_in_second = d.pop("periodInSecond")

        performance_analyser_record = cls(
            id=id,
            analyser_id=analyser_id,
            average=average,
            min_=min_,
            max_=max_,
            date=date,
            period_in_second=period_in_second,
        )

        return performance_analyser_record
