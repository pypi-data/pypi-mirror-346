from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.counted_equipment_ordered_line import CountedEquipmentOrderedLine
    from ..models.criteria_string import CriteriaString


T = TypeVar("T", bound="CountedEquipmentOrderedBy")


@_attrs_define
class CountedEquipmentOrderedBy:
    """
    Attributes:
        order_by_fields (list['CriteriaString']):
        lines (list['CountedEquipmentOrderedLine']):
    """

    order_by_fields: list["CriteriaString"]
    lines: list["CountedEquipmentOrderedLine"]

    def to_dict(self) -> dict[str, Any]:
        order_by_fields = []
        for order_by_fields_item_data in self.order_by_fields:
            order_by_fields_item = order_by_fields_item_data.to_dict()
            order_by_fields.append(order_by_fields_item)

        lines = []
        for lines_item_data in self.lines:
            lines_item = lines_item_data.to_dict()
            lines.append(lines_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "orderByFields": order_by_fields,
                "lines": lines,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.counted_equipment_ordered_line import CountedEquipmentOrderedLine
        from ..models.criteria_string import CriteriaString

        d = dict(src_dict)
        order_by_fields = []
        _order_by_fields = d.pop("orderByFields")
        for order_by_fields_item_data in _order_by_fields:
            order_by_fields_item = CriteriaString.from_dict(order_by_fields_item_data)

            order_by_fields.append(order_by_fields_item)

        lines = []
        _lines = d.pop("lines")
        for lines_item_data in _lines:
            lines_item = CountedEquipmentOrderedLine.from_dict(lines_item_data)

            lines.append(lines_item)

        counted_equipment_ordered_by = cls(
            order_by_fields=order_by_fields,
            lines=lines,
        )

        return counted_equipment_ordered_by
