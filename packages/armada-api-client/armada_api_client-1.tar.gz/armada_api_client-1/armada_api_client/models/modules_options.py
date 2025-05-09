from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModulesOptions")


@_attrs_define
class ModulesOptions:
    """
    Attributes:
        node_red (Union[None, Unset, str]):
    """

    node_red: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        node_red: Union[None, Unset, str]
        if isinstance(self.node_red, Unset):
            node_red = UNSET
        else:
            node_red = self.node_red

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if node_red is not UNSET:
            field_dict["nodeRed"] = node_red

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_node_red(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_red = _parse_node_red(d.pop("nodeRed", UNSET))

        modules_options = cls(
            node_red=node_red,
        )

        return modules_options
