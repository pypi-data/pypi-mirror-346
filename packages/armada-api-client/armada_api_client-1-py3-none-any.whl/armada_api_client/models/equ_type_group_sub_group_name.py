from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="EquTypeGroupSubGroupName")


@_attrs_define
class EquTypeGroupSubGroupName:
    """
    Attributes:
        equ_type (str):
        group (str):
        sub_group (str):
        name (str):
    """

    equ_type: str
    group: str
    sub_group: str
    name: str

    def to_dict(self) -> dict[str, Any]:
        equ_type = self.equ_type

        group = self.group

        sub_group = self.sub_group

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "equType": equ_type,
                "group": group,
                "subGroup": sub_group,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        equ_type = d.pop("equType")

        group = d.pop("group")

        sub_group = d.pop("subGroup")

        name = d.pop("name")

        equ_type_group_sub_group_name = cls(
            equ_type=equ_type,
            group=group,
            sub_group=sub_group,
            name=name,
        )

        return equ_type_group_sub_group_name
