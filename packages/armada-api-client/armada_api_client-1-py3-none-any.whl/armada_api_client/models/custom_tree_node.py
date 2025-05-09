from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CustomTreeNode")


@_attrs_define
class CustomTreeNode:
    """
    Attributes:
        id (str):
        node_id (int):
        parent_id (int):
        name (str):
    """

    id: str
    node_id: int
    parent_id: int
    name: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        node_id = self.node_id

        parent_id = self.parent_id

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "nodeId": node_id,
                "parentId": parent_id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        node_id = d.pop("nodeId")

        parent_id = d.pop("parentId")

        name = d.pop("name")

        custom_tree_node = cls(
            id=id,
            node_id=node_id,
            parent_id=parent_id,
            name=name,
        )

        return custom_tree_node
