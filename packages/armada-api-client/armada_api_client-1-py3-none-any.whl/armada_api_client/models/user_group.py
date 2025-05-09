from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_role import UserRole


T = TypeVar("T", bound="UserGroup")


@_attrs_define
class UserGroup:
    """
    Attributes:
        id (str):
        group_id (int):
        name (str):
        ldap_group (Union[None, Unset, str]):
        user_roles (Union[None, Unset, list['UserRole']]):
    """

    id: str
    group_id: int
    name: str
    ldap_group: Union[None, Unset, str] = UNSET
    user_roles: Union[None, Unset, list["UserRole"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        group_id = self.group_id

        name = self.name

        ldap_group: Union[None, Unset, str]
        if isinstance(self.ldap_group, Unset):
            ldap_group = UNSET
        else:
            ldap_group = self.ldap_group

        user_roles: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.user_roles, Unset):
            user_roles = UNSET
        elif isinstance(self.user_roles, list):
            user_roles = []
            for user_roles_type_0_item_data in self.user_roles:
                user_roles_type_0_item = user_roles_type_0_item_data.to_dict()
                user_roles.append(user_roles_type_0_item)

        else:
            user_roles = self.user_roles

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "groupId": group_id,
                "name": name,
            }
        )
        if ldap_group is not UNSET:
            field_dict["ldapGroup"] = ldap_group
        if user_roles is not UNSET:
            field_dict["userRoles"] = user_roles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_role import UserRole

        d = dict(src_dict)
        id = d.pop("id")

        group_id = d.pop("groupId")

        name = d.pop("name")

        def _parse_ldap_group(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ldap_group = _parse_ldap_group(d.pop("ldapGroup", UNSET))

        def _parse_user_roles(data: object) -> Union[None, Unset, list["UserRole"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                user_roles_type_0 = []
                _user_roles_type_0 = data
                for user_roles_type_0_item_data in _user_roles_type_0:
                    user_roles_type_0_item = UserRole.from_dict(user_roles_type_0_item_data)

                    user_roles_type_0.append(user_roles_type_0_item)

                return user_roles_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["UserRole"]], data)

        user_roles = _parse_user_roles(d.pop("userRoles", UNSET))

        user_group = cls(
            id=id,
            group_id=group_id,
            name=name,
            ldap_group=ldap_group,
            user_roles=user_roles,
        )

        return user_group
