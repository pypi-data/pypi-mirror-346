from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DataRecordSelectionInfo")


@_attrs_define
class DataRecordSelectionInfo:
    """
    Attributes:
        equipment_type (str):
        data_record_name (str):
        data_record_group (str):
        data_record_subgroup (str):
        resolution (str):
        record_type (str):
        equ_id (int):
        equipment_path (str):
    """

    equipment_type: str
    data_record_name: str
    data_record_group: str
    data_record_subgroup: str
    resolution: str
    record_type: str
    equ_id: int
    equipment_path: str

    def to_dict(self) -> dict[str, Any]:
        equipment_type = self.equipment_type

        data_record_name = self.data_record_name

        data_record_group = self.data_record_group

        data_record_subgroup = self.data_record_subgroup

        resolution = self.resolution

        record_type = self.record_type

        equ_id = self.equ_id

        equipment_path = self.equipment_path

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "equipmentType": equipment_type,
                "dataRecordName": data_record_name,
                "dataRecordGroup": data_record_group,
                "dataRecordSubgroup": data_record_subgroup,
                "resolution": resolution,
                "recordType": record_type,
                "equId": equ_id,
                "equipmentPath": equipment_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        equipment_type = d.pop("equipmentType")

        data_record_name = d.pop("dataRecordName")

        data_record_group = d.pop("dataRecordGroup")

        data_record_subgroup = d.pop("dataRecordSubgroup")

        resolution = d.pop("resolution")

        record_type = d.pop("recordType")

        equ_id = d.pop("equId")

        equipment_path = d.pop("equipmentPath")

        data_record_selection_info = cls(
            equipment_type=equipment_type,
            data_record_name=data_record_name,
            data_record_group=data_record_group,
            data_record_subgroup=data_record_subgroup,
            resolution=resolution,
            record_type=record_type,
            equ_id=equ_id,
            equipment_path=equipment_path,
        )

        return data_record_selection_info
