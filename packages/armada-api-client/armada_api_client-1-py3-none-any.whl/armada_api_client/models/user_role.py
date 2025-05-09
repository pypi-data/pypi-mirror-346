from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UserRole")


@_attrs_define
class UserRole:
    """
    Attributes:
        role_id (int):
        name (str):
    """

    role_id: int
    name: str

    def to_dict(self) -> dict[str, Any]:
        role_id = self.role_id

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "roleId": role_id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role_id = d.pop("roleId")

        name = d.pop("name")

        user_role = cls(
            role_id=role_id,
            name=name,
        )

        return user_role
