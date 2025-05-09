from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthInfo")


@_attrs_define
class AuthInfo:
    """
    Attributes:
        tenant (Union[None, Unset, str]):
        login (Union[None, Unset, str]):
        password (Union[None, Unset, str]):
    """

    tenant: Union[None, Unset, str] = UNSET
    login: Union[None, Unset, str] = UNSET
    password: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        tenant: Union[None, Unset, str]
        if isinstance(self.tenant, Unset):
            tenant = UNSET
        else:
            tenant = self.tenant

        login: Union[None, Unset, str]
        if isinstance(self.login, Unset):
            login = UNSET
        else:
            login = self.login

        password: Union[None, Unset, str]
        if isinstance(self.password, Unset):
            password = UNSET
        else:
            password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if login is not UNSET:
            field_dict["login"] = login
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_tenant(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tenant = _parse_tenant(d.pop("tenant", UNSET))

        def _parse_login(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        login = _parse_login(d.pop("login", UNSET))

        def _parse_password(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        password = _parse_password(d.pop("password", UNSET))

        auth_info = cls(
            tenant=tenant,
            login=login,
            password=password,
        )

        return auth_info
