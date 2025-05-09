import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_config import UserConfig


T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        id (str):
        user_id (int):
        login (str):
        first_name (Union[None, str]):
        last_name (Union[None, str]):
        mail (Union[None, str]):
        phone (Union[None, str]):
        language (Union[None, str]):
        group_id (int):
        auth_source (int):
        password (Union[None, Unset, str]):
        last_connection (Union[None, Unset, datetime.datetime]):
        group_name (Union[None, Unset, str]):
        roles (Union[None, Unset, list[str]]):
        user_config (Union['UserConfig', None, Unset]):
        tenant (Union[None, Unset, str]):
        tenant_actual (Union[None, Unset, str]):
        tenants (Union[None, Unset, list[str]]):
    """

    id: str
    user_id: int
    login: str
    first_name: Union[None, str]
    last_name: Union[None, str]
    mail: Union[None, str]
    phone: Union[None, str]
    language: Union[None, str]
    group_id: int
    auth_source: int
    password: Union[None, Unset, str] = UNSET
    last_connection: Union[None, Unset, datetime.datetime] = UNSET
    group_name: Union[None, Unset, str] = UNSET
    roles: Union[None, Unset, list[str]] = UNSET
    user_config: Union["UserConfig", None, Unset] = UNSET
    tenant: Union[None, Unset, str] = UNSET
    tenant_actual: Union[None, Unset, str] = UNSET
    tenants: Union[None, Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_config import UserConfig

        id = self.id

        user_id = self.user_id

        login = self.login

        first_name: Union[None, str]
        first_name = self.first_name

        last_name: Union[None, str]
        last_name = self.last_name

        mail: Union[None, str]
        mail = self.mail

        phone: Union[None, str]
        phone = self.phone

        language: Union[None, str]
        language = self.language

        group_id = self.group_id

        auth_source = self.auth_source

        password: Union[None, Unset, str]
        if isinstance(self.password, Unset):
            password = UNSET
        else:
            password = self.password

        last_connection: Union[None, Unset, str]
        if isinstance(self.last_connection, Unset):
            last_connection = UNSET
        elif isinstance(self.last_connection, datetime.datetime):
            last_connection = self.last_connection.isoformat()
        else:
            last_connection = self.last_connection

        group_name: Union[None, Unset, str]
        if isinstance(self.group_name, Unset):
            group_name = UNSET
        else:
            group_name = self.group_name

        roles: Union[None, Unset, list[str]]
        if isinstance(self.roles, Unset):
            roles = UNSET
        elif isinstance(self.roles, list):
            roles = self.roles

        else:
            roles = self.roles

        user_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.user_config, Unset):
            user_config = UNSET
        elif isinstance(self.user_config, UserConfig):
            user_config = self.user_config.to_dict()
        else:
            user_config = self.user_config

        tenant: Union[None, Unset, str]
        if isinstance(self.tenant, Unset):
            tenant = UNSET
        else:
            tenant = self.tenant

        tenant_actual: Union[None, Unset, str]
        if isinstance(self.tenant_actual, Unset):
            tenant_actual = UNSET
        else:
            tenant_actual = self.tenant_actual

        tenants: Union[None, Unset, list[str]]
        if isinstance(self.tenants, Unset):
            tenants = UNSET
        elif isinstance(self.tenants, list):
            tenants = self.tenants

        else:
            tenants = self.tenants

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "userId": user_id,
                "login": login,
                "firstName": first_name,
                "lastName": last_name,
                "mail": mail,
                "phone": phone,
                "language": language,
                "groupId": group_id,
                "authSource": auth_source,
            }
        )
        if password is not UNSET:
            field_dict["password"] = password
        if last_connection is not UNSET:
            field_dict["lastConnection"] = last_connection
        if group_name is not UNSET:
            field_dict["groupName"] = group_name
        if roles is not UNSET:
            field_dict["roles"] = roles
        if user_config is not UNSET:
            field_dict["userConfig"] = user_config
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if tenant_actual is not UNSET:
            field_dict["tenantActual"] = tenant_actual
        if tenants is not UNSET:
            field_dict["tenants"] = tenants

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_config import UserConfig

        d = dict(src_dict)
        id = d.pop("id")

        user_id = d.pop("userId")

        login = d.pop("login")

        def _parse_first_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        first_name = _parse_first_name(d.pop("firstName"))

        def _parse_last_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        last_name = _parse_last_name(d.pop("lastName"))

        def _parse_mail(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        mail = _parse_mail(d.pop("mail"))

        def _parse_phone(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        phone = _parse_phone(d.pop("phone"))

        def _parse_language(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        language = _parse_language(d.pop("language"))

        group_id = d.pop("groupId")

        auth_source = d.pop("authSource")

        def _parse_password(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        password = _parse_password(d.pop("password", UNSET))

        def _parse_last_connection(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_connection_type_0 = isoparse(data)

                return last_connection_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_connection = _parse_last_connection(d.pop("lastConnection", UNSET))

        def _parse_group_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_name = _parse_group_name(d.pop("groupName", UNSET))

        def _parse_roles(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                roles_type_0 = cast(list[str], data)

                return roles_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        roles = _parse_roles(d.pop("roles", UNSET))

        def _parse_user_config(data: object) -> Union["UserConfig", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_config_type_1 = UserConfig.from_dict(data)

                return user_config_type_1
            except:  # noqa: E722
                pass
            return cast(Union["UserConfig", None, Unset], data)

        user_config = _parse_user_config(d.pop("userConfig", UNSET))

        def _parse_tenant(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tenant = _parse_tenant(d.pop("tenant", UNSET))

        def _parse_tenant_actual(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tenant_actual = _parse_tenant_actual(d.pop("tenantActual", UNSET))

        def _parse_tenants(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tenants_type_0 = cast(list[str], data)

                return tenants_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tenants = _parse_tenants(d.pop("tenants", UNSET))

        user = cls(
            id=id,
            user_id=user_id,
            login=login,
            first_name=first_name,
            last_name=last_name,
            mail=mail,
            phone=phone,
            language=language,
            group_id=group_id,
            auth_source=auth_source,
            password=password,
            last_connection=last_connection,
            group_name=group_name,
            roles=roles,
            user_config=user_config,
            tenant=tenant,
            tenant_actual=tenant_actual,
            tenants=tenants,
        )

        return user
