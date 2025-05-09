from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PathRelGroupSubGroupName")


@_attrs_define
class PathRelGroupSubGroupName:
    """
    Attributes:
        path_rel (str):
        group (str):
        sub_group (str):
        name (str):
    """

    path_rel: str
    group: str
    sub_group: str
    name: str

    def to_dict(self) -> dict[str, Any]:
        path_rel = self.path_rel

        group = self.group

        sub_group = self.sub_group

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "pathRel": path_rel,
                "group": group,
                "subGroup": sub_group,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path_rel = d.pop("pathRel")

        group = d.pop("group")

        sub_group = d.pop("subGroup")

        name = d.pop("name")

        path_rel_group_sub_group_name = cls(
            path_rel=path_rel,
            group=group,
            sub_group=sub_group,
            name=name,
        )

        return path_rel_group_sub_group_name
