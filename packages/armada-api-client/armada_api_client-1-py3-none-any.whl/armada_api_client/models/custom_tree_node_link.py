from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CustomTreeNodeLink")


@_attrs_define
class CustomTreeNodeLink:
    """
    Attributes:
        id (str):
        link_id (int):
        equ_id (int):
        custom_tree_node_id (int):
    """

    id: str
    link_id: int
    equ_id: int
    custom_tree_node_id: int

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        link_id = self.link_id

        equ_id = self.equ_id

        custom_tree_node_id = self.custom_tree_node_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "linkId": link_id,
                "equId": equ_id,
                "customTreeNodeId": custom_tree_node_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        link_id = d.pop("linkId")

        equ_id = d.pop("equId")

        custom_tree_node_id = d.pop("customTreeNodeId")

        custom_tree_node_link = cls(
            id=id,
            link_id=link_id,
            equ_id=equ_id,
            custom_tree_node_id=custom_tree_node_id,
        )

        return custom_tree_node_link
