from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DataRecordsSelectionInfo")


@_attrs_define
class DataRecordsSelectionInfo:
    """
    Attributes:
        path_rel (str):
        data_name (str):
        data_group (str):
        data_subgroup (str):
        resolution (str):
        record_type (str):
        list_of_equ_ids (Union[None, Unset, list[int]]):
    """

    path_rel: str
    data_name: str
    data_group: str
    data_subgroup: str
    resolution: str
    record_type: str
    list_of_equ_ids: Union[None, Unset, list[int]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        path_rel = self.path_rel

        data_name = self.data_name

        data_group = self.data_group

        data_subgroup = self.data_subgroup

        resolution = self.resolution

        record_type = self.record_type

        list_of_equ_ids: Union[None, Unset, list[int]]
        if isinstance(self.list_of_equ_ids, Unset):
            list_of_equ_ids = UNSET
        elif isinstance(self.list_of_equ_ids, list):
            list_of_equ_ids = self.list_of_equ_ids

        else:
            list_of_equ_ids = self.list_of_equ_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "pathRel": path_rel,
                "dataName": data_name,
                "dataGroup": data_group,
                "dataSubgroup": data_subgroup,
                "resolution": resolution,
                "recordType": record_type,
            }
        )
        if list_of_equ_ids is not UNSET:
            field_dict["listOfEquIds"] = list_of_equ_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path_rel = d.pop("pathRel")

        data_name = d.pop("dataName")

        data_group = d.pop("dataGroup")

        data_subgroup = d.pop("dataSubgroup")

        resolution = d.pop("resolution")

        record_type = d.pop("recordType")

        def _parse_list_of_equ_ids(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                list_of_equ_ids_type_0 = cast(list[int], data)

                return list_of_equ_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        list_of_equ_ids = _parse_list_of_equ_ids(d.pop("listOfEquIds", UNSET))

        data_records_selection_info = cls(
            path_rel=path_rel,
            data_name=data_name,
            data_group=data_group,
            data_subgroup=data_subgroup,
            resolution=resolution,
            record_type=record_type,
            list_of_equ_ids=list_of_equ_ids,
        )

        return data_records_selection_info
