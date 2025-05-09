from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ElementModificationRequest")


@_attrs_define
class ElementModificationRequest:
    """
    Attributes:
        new_value (str):
        equipment_path (str):
        equ_id (int):
        table_name (str):
        attribute_name (str):
        element_id (int):
        element_group (Union[None, Unset, str]):
        element_subgroup (Union[None, Unset, str]):
        element_name (Union[None, Unset, str]):
    """

    new_value: str
    equipment_path: str
    equ_id: int
    table_name: str
    attribute_name: str
    element_id: int
    element_group: Union[None, Unset, str] = UNSET
    element_subgroup: Union[None, Unset, str] = UNSET
    element_name: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        new_value = self.new_value

        equipment_path = self.equipment_path

        equ_id = self.equ_id

        table_name = self.table_name

        attribute_name = self.attribute_name

        element_id = self.element_id

        element_group: Union[None, Unset, str]
        if isinstance(self.element_group, Unset):
            element_group = UNSET
        else:
            element_group = self.element_group

        element_subgroup: Union[None, Unset, str]
        if isinstance(self.element_subgroup, Unset):
            element_subgroup = UNSET
        else:
            element_subgroup = self.element_subgroup

        element_name: Union[None, Unset, str]
        if isinstance(self.element_name, Unset):
            element_name = UNSET
        else:
            element_name = self.element_name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "newValue": new_value,
                "equipmentPath": equipment_path,
                "equId": equ_id,
                "tableName": table_name,
                "attributeName": attribute_name,
                "elementId": element_id,
            }
        )
        if element_group is not UNSET:
            field_dict["elementGroup"] = element_group
        if element_subgroup is not UNSET:
            field_dict["elementSubgroup"] = element_subgroup
        if element_name is not UNSET:
            field_dict["elementName"] = element_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        new_value = d.pop("newValue")

        equipment_path = d.pop("equipmentPath")

        equ_id = d.pop("equId")

        table_name = d.pop("tableName")

        attribute_name = d.pop("attributeName")

        element_id = d.pop("elementId")

        def _parse_element_group(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        element_group = _parse_element_group(d.pop("elementGroup", UNSET))

        def _parse_element_subgroup(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        element_subgroup = _parse_element_subgroup(d.pop("elementSubgroup", UNSET))

        def _parse_element_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        element_name = _parse_element_name(d.pop("elementName", UNSET))

        element_modification_request = cls(
            new_value=new_value,
            equipment_path=equipment_path,
            equ_id=equ_id,
            table_name=table_name,
            attribute_name=attribute_name,
            element_id=element_id,
            element_group=element_group,
            element_subgroup=element_subgroup,
            element_name=element_name,
        )

        return element_modification_request
