from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="CountedEquipmentOrderedLine")


@_attrs_define
class CountedEquipmentOrderedLine:
    """
    Attributes:
        order_by_values (list[str]):
        count (int):
    """

    order_by_values: list[str]
    count: int

    def to_dict(self) -> dict[str, Any]:
        order_by_values = self.order_by_values

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "orderByValues": order_by_values,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        order_by_values = cast(list[str], d.pop("orderByValues"))

        count = d.pop("count")

        counted_equipment_ordered_line = cls(
            order_by_values=order_by_values,
            count=count,
        )

        return counted_equipment_ordered_line
