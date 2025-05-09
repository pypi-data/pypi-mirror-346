from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantSetting")


@_attrs_define
class TenantSetting:
    """
    Attributes:
        group (Union[None, str]):
        name (Union[None, str]):
        description (Union[None, str]):
        value (Union[None, Unset, str]):
        id (Union[None, Unset, str]):
    """

    group: Union[None, str]
    name: Union[None, str]
    description: Union[None, str]
    value: Union[None, Unset, str] = UNSET
    id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        group: Union[None, str]
        group = self.group

        name: Union[None, str]
        name = self.name

        description: Union[None, str]
        description = self.description

        value: Union[None, Unset, str]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "group": group,
                "name": name,
                "description": description,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_group(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        group = _parse_group(d.pop("group"))

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        def _parse_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        value = _parse_value(d.pop("value", UNSET))

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        tenant_setting = cls(
            group=group,
            name=name,
            description=description,
            value=value,
            id=id,
        )

        return tenant_setting
