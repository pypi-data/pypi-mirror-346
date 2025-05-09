import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="DataRecordConsolidationInfo")


@_attrs_define
class DataRecordConsolidationInfo:
    """
    Attributes:
        group_y_axis_records_by (str):
        group_x_axis_records_by (str):
        group_method_y (str):
        group_method_x (str):
        start_date (datetime.datetime):
        end_date (datetime.datetime):
    """

    group_y_axis_records_by: str
    group_x_axis_records_by: str
    group_method_y: str
    group_method_x: str
    start_date: datetime.datetime
    end_date: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        group_y_axis_records_by = self.group_y_axis_records_by

        group_x_axis_records_by = self.group_x_axis_records_by

        group_method_y = self.group_method_y

        group_method_x = self.group_method_x

        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "groupYAxisRecordsBy": group_y_axis_records_by,
                "groupXAxisRecordsBy": group_x_axis_records_by,
                "groupMethodY": group_method_y,
                "groupMethodX": group_method_x,
                "startDate": start_date,
                "endDate": end_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group_y_axis_records_by = d.pop("groupYAxisRecordsBy")

        group_x_axis_records_by = d.pop("groupXAxisRecordsBy")

        group_method_y = d.pop("groupMethodY")

        group_method_x = d.pop("groupMethodX")

        start_date = isoparse(d.pop("startDate"))

        end_date = isoparse(d.pop("endDate"))

        data_record_consolidation_info = cls(
            group_y_axis_records_by=group_y_axis_records_by,
            group_x_axis_records_by=group_x_axis_records_by,
            group_method_y=group_method_y,
            group_method_x=group_method_x,
            start_date=start_date,
            end_date=end_date,
        )

        return data_record_consolidation_info
