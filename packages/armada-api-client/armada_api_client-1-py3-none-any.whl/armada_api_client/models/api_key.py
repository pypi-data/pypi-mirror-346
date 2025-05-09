from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_date_and_user import AuditDateAndUser


T = TypeVar("T", bound="ApiKey")


@_attrs_define
class ApiKey:
    """
    Attributes:
        id (str):
        key_id (int):
        description (str):
        group_id (int):
        audit (Union['AuditDateAndUser', None, Unset]):
        key (Union[None, Unset, str]):
    """

    id: str
    key_id: int
    description: str
    group_id: int
    audit: Union["AuditDateAndUser", None, Unset] = UNSET
    key: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_date_and_user import AuditDateAndUser

        id = self.id

        key_id = self.key_id

        description = self.description

        group_id = self.group_id

        audit: Union[None, Unset, dict[str, Any]]
        if isinstance(self.audit, Unset):
            audit = UNSET
        elif isinstance(self.audit, AuditDateAndUser):
            audit = self.audit.to_dict()
        else:
            audit = self.audit

        key: Union[None, Unset, str]
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "keyId": key_id,
                "description": description,
                "groupId": group_id,
            }
        )
        if audit is not UNSET:
            field_dict["audit"] = audit
        if key is not UNSET:
            field_dict["key"] = key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_date_and_user import AuditDateAndUser

        d = dict(src_dict)
        id = d.pop("id")

        key_id = d.pop("keyId")

        description = d.pop("description")

        group_id = d.pop("groupId")

        def _parse_audit(data: object) -> Union["AuditDateAndUser", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                audit_type_1 = AuditDateAndUser.from_dict(data)

                return audit_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AuditDateAndUser", None, Unset], data)

        audit = _parse_audit(d.pop("audit", UNSET))

        def _parse_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        key = _parse_key(d.pop("key", UNSET))

        api_key = cls(
            id=id,
            key_id=key_id,
            description=description,
            group_id=group_id,
            audit=audit,
            key=key,
        )

        return api_key
