from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="EntProp")


@_attrs_define
class EntProp:
    """
    Attributes:
        entity (str):
        property_ (str):
    """

    entity: str
    property_: str

    def to_dict(self) -> dict[str, Any]:
        entity = self.entity

        property_ = self.property_

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "entity": entity,
                "property": property_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        entity = d.pop("entity")

        property_ = d.pop("property")

        ent_prop = cls(
            entity=entity,
            property_=property_,
        )

        return ent_prop
