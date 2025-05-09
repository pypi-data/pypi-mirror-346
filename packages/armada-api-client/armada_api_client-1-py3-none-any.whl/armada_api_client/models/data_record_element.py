import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="DataRecordElement")


@_attrs_define
class DataRecordElement:
    """
    Attributes:
        equ_id_data_id (str):
        id (str):
        dt (datetime.datetime):
        equ_id (int):
        data_id (int):
        value (float):
        value_min (float):
        value_max (float):
    """

    equ_id_data_id: str
    id: str
    dt: datetime.datetime
    equ_id: int
    data_id: int
    value: float
    value_min: float
    value_max: float

    def to_dict(self) -> dict[str, Any]:
        equ_id_data_id = self.equ_id_data_id

        id = self.id

        dt = self.dt.isoformat()

        equ_id = self.equ_id

        data_id = self.data_id

        value = self.value

        value_min = self.value_min

        value_max = self.value_max

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "equIdDataId": equ_id_data_id,
                "id": id,
                "dt": dt,
                "equId": equ_id,
                "dataId": data_id,
                "value": value,
                "valueMin": value_min,
                "valueMax": value_max,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        equ_id_data_id = d.pop("equIdDataId")

        id = d.pop("id")

        dt = isoparse(d.pop("dt"))

        equ_id = d.pop("equId")

        data_id = d.pop("dataId")

        value = d.pop("value")

        value_min = d.pop("valueMin")

        value_max = d.pop("valueMax")

        data_record_element = cls(
            equ_id_data_id=equ_id_data_id,
            id=id,
            dt=dt,
            equ_id=equ_id,
            data_id=data_id,
            value=value,
            value_min=value_min,
            value_max=value_max,
        )

        return data_record_element
