import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.data_record_selection_info import DataRecordSelectionInfo


T = TypeVar("T", bound="DataRecordsExtented")


@_attrs_define
class DataRecordsExtented:
    """
    Attributes:
        data_record_selection_info (list['DataRecordSelectionInfo']):
        extented_arrays_of_values (list[list[float]]):
        date_times (list[datetime.datetime]):
    """

    data_record_selection_info: list["DataRecordSelectionInfo"]
    extented_arrays_of_values: list[list[float]]
    date_times: list[datetime.datetime]

    def to_dict(self) -> dict[str, Any]:
        data_record_selection_info = []
        for data_record_selection_info_item_data in self.data_record_selection_info:
            data_record_selection_info_item = data_record_selection_info_item_data.to_dict()
            data_record_selection_info.append(data_record_selection_info_item)

        extented_arrays_of_values = []
        for extented_arrays_of_values_item_data in self.extented_arrays_of_values:
            extented_arrays_of_values_item = extented_arrays_of_values_item_data

            extented_arrays_of_values.append(extented_arrays_of_values_item)

        date_times = []
        for date_times_item_data in self.date_times:
            date_times_item = date_times_item_data.isoformat()
            date_times.append(date_times_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "dataRecordSelectionInfo": data_record_selection_info,
                "extentedArraysOfValues": extented_arrays_of_values,
                "dateTimes": date_times,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_record_selection_info import DataRecordSelectionInfo

        d = dict(src_dict)
        data_record_selection_info = []
        _data_record_selection_info = d.pop("dataRecordSelectionInfo")
        for data_record_selection_info_item_data in _data_record_selection_info:
            data_record_selection_info_item = DataRecordSelectionInfo.from_dict(data_record_selection_info_item_data)

            data_record_selection_info.append(data_record_selection_info_item)

        extented_arrays_of_values = []
        _extented_arrays_of_values = d.pop("extentedArraysOfValues")
        for extented_arrays_of_values_item_data in _extented_arrays_of_values:
            extented_arrays_of_values_item = cast(list[float], extented_arrays_of_values_item_data)

            extented_arrays_of_values.append(extented_arrays_of_values_item)

        date_times = []
        _date_times = d.pop("dateTimes")
        for date_times_item_data in _date_times:
            date_times_item = isoparse(date_times_item_data)

            date_times.append(date_times_item)

        data_records_extented = cls(
            data_record_selection_info=data_record_selection_info,
            extented_arrays_of_values=extented_arrays_of_values,
            date_times=date_times,
        )

        return data_records_extented
