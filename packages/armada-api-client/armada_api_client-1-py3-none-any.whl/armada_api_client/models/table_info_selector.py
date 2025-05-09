from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="TableInfoSelector")


@_attrs_define
class TableInfoSelector:
    """
    Attributes:
        target_table (str):
        name (str):
        group (str):
        subgroup (str):
        export_name (str):
        distinct_property (str):
    """

    target_table: str
    name: str
    group: str
    subgroup: str
    export_name: str
    distinct_property: str

    def to_dict(self) -> dict[str, Any]:
        target_table = self.target_table

        name = self.name

        group = self.group

        subgroup = self.subgroup

        export_name = self.export_name

        distinct_property = self.distinct_property

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "targetTable": target_table,
                "name": name,
                "group": group,
                "subgroup": subgroup,
                "exportName": export_name,
                "distinctProperty": distinct_property,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_table = d.pop("targetTable")

        name = d.pop("name")

        group = d.pop("group")

        subgroup = d.pop("subgroup")

        export_name = d.pop("exportName")

        distinct_property = d.pop("distinctProperty")

        table_info_selector = cls(
            target_table=target_table,
            name=name,
            group=group,
            subgroup=subgroup,
            export_name=export_name,
            distinct_property=distinct_property,
        )

        return table_info_selector
