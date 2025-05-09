from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ent_prop import EntProp


T = TypeVar("T", bound="CriteriaString")


@_attrs_define
class CriteriaString:
    """
    Attributes:
        ent_prop (EntProp):
        value (Union[None, Unset, str]):
    """

    ent_prop: "EntProp"
    value: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        ent_prop = self.ent_prop.to_dict()

        value: Union[None, Unset, str]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "entProp": ent_prop,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ent_prop import EntProp

        d = dict(src_dict)
        ent_prop = EntProp.from_dict(d.pop("entProp"))

        def _parse_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        value = _parse_value(d.pop("value", UNSET))

        criteria_string = cls(
            ent_prop=ent_prop,
            value=value,
        )

        return criteria_string
