import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="DataRecordReport")


@_attrs_define
class DataRecordReport:
    """
    Attributes:
        date_times (list[datetime.datetime]):
        grouping_names (list[str]):
        values (list[list[float]]):
        title (str):
        title_y (str):
        title_x (str):
        value_summarized_by_group_global (float):
        values_summurized_by_group (list[float]):
    """

    date_times: list[datetime.datetime]
    grouping_names: list[str]
    values: list[list[float]]
    title: str
    title_y: str
    title_x: str
    value_summarized_by_group_global: float
    values_summurized_by_group: list[float]

    def to_dict(self) -> dict[str, Any]:
        date_times = []
        for date_times_item_data in self.date_times:
            date_times_item = date_times_item_data.isoformat()
            date_times.append(date_times_item)

        grouping_names = self.grouping_names

        values = []
        for values_item_data in self.values:
            values_item = values_item_data

            values.append(values_item)

        title = self.title

        title_y = self.title_y

        title_x = self.title_x

        value_summarized_by_group_global = self.value_summarized_by_group_global

        values_summurized_by_group = self.values_summurized_by_group

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "dateTimes": date_times,
                "groupingNames": grouping_names,
                "values": values,
                "title": title,
                "titleY": title_y,
                "titleX": title_x,
                "valueSummarizedByGroupGlobal": value_summarized_by_group_global,
                "valuesSummurizedByGroup": values_summurized_by_group,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date_times = []
        _date_times = d.pop("dateTimes")
        for date_times_item_data in _date_times:
            date_times_item = isoparse(date_times_item_data)

            date_times.append(date_times_item)

        grouping_names = cast(list[str], d.pop("groupingNames"))

        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = cast(list[float], values_item_data)

            values.append(values_item)

        title = d.pop("title")

        title_y = d.pop("titleY")

        title_x = d.pop("titleX")

        value_summarized_by_group_global = d.pop("valueSummarizedByGroupGlobal")

        values_summurized_by_group = cast(list[float], d.pop("valuesSummurizedByGroup"))

        data_record_report = cls(
            date_times=date_times,
            grouping_names=grouping_names,
            values=values,
            title=title,
            title_y=title_y,
            title_x=title_x,
            value_summarized_by_group_global=value_summarized_by_group_global,
            values_summurized_by_group=values_summurized_by_group,
        )

        return data_record_report
