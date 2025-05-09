from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Metric")


@_attrs_define
class Metric:
    """
    Attributes:
        type_ (Union[None, Unset, str]):
        key (Union[None, Unset, str]):
        unit (Union[None, Unset, str]):
        api_enpoint_example (Union[None, Unset, str]):
    """

    type_: Union[None, Unset, str] = UNSET
    key: Union[None, Unset, str] = UNSET
    unit: Union[None, Unset, str] = UNSET
    api_enpoint_example: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        key: Union[None, Unset, str]
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        unit: Union[None, Unset, str]
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        api_enpoint_example: Union[None, Unset, str]
        if isinstance(self.api_enpoint_example, Unset):
            api_enpoint_example = UNSET
        else:
            api_enpoint_example = self.api_enpoint_example

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if key is not UNSET:
            field_dict["key"] = key
        if unit is not UNSET:
            field_dict["unit"] = unit
        if api_enpoint_example is not UNSET:
            field_dict["apiEnpointExample"] = api_enpoint_example

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_type_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        key = _parse_key(d.pop("key", UNSET))

        def _parse_unit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        unit = _parse_unit(d.pop("unit", UNSET))

        def _parse_api_enpoint_example(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_enpoint_example = _parse_api_enpoint_example(d.pop("apiEnpointExample", UNSET))

        metric = cls(
            type_=type_,
            key=key,
            unit=unit,
            api_enpoint_example=api_enpoint_example,
        )

        return metric
