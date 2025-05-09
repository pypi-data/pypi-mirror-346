from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantRegistrationInfoDto")


@_attrs_define
class TenantRegistrationInfoDto:
    """
    Attributes:
        organization (Union[None, Unset, str]):
        admin_email (Union[None, Unset, str]):
        admin_password (Union[None, Unset, str]):
        admin_first_name (Union[None, Unset, str]):
        admin_last_name (Union[None, Unset, str]):
        frontend_theme (Union[None, Unset, str]):
        delegated_access_partner (Union[None, Unset, str]):
    """

    organization: Union[None, Unset, str] = UNSET
    admin_email: Union[None, Unset, str] = UNSET
    admin_password: Union[None, Unset, str] = UNSET
    admin_first_name: Union[None, Unset, str] = UNSET
    admin_last_name: Union[None, Unset, str] = UNSET
    frontend_theme: Union[None, Unset, str] = UNSET
    delegated_access_partner: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        organization: Union[None, Unset, str]
        if isinstance(self.organization, Unset):
            organization = UNSET
        else:
            organization = self.organization

        admin_email: Union[None, Unset, str]
        if isinstance(self.admin_email, Unset):
            admin_email = UNSET
        else:
            admin_email = self.admin_email

        admin_password: Union[None, Unset, str]
        if isinstance(self.admin_password, Unset):
            admin_password = UNSET
        else:
            admin_password = self.admin_password

        admin_first_name: Union[None, Unset, str]
        if isinstance(self.admin_first_name, Unset):
            admin_first_name = UNSET
        else:
            admin_first_name = self.admin_first_name

        admin_last_name: Union[None, Unset, str]
        if isinstance(self.admin_last_name, Unset):
            admin_last_name = UNSET
        else:
            admin_last_name = self.admin_last_name

        frontend_theme: Union[None, Unset, str]
        if isinstance(self.frontend_theme, Unset):
            frontend_theme = UNSET
        else:
            frontend_theme = self.frontend_theme

        delegated_access_partner: Union[None, Unset, str]
        if isinstance(self.delegated_access_partner, Unset):
            delegated_access_partner = UNSET
        else:
            delegated_access_partner = self.delegated_access_partner

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if organization is not UNSET:
            field_dict["organization"] = organization
        if admin_email is not UNSET:
            field_dict["adminEmail"] = admin_email
        if admin_password is not UNSET:
            field_dict["adminPassword"] = admin_password
        if admin_first_name is not UNSET:
            field_dict["adminFirstName"] = admin_first_name
        if admin_last_name is not UNSET:
            field_dict["adminLastName"] = admin_last_name
        if frontend_theme is not UNSET:
            field_dict["frontendTheme"] = frontend_theme
        if delegated_access_partner is not UNSET:
            field_dict["delegatedAccessPartner"] = delegated_access_partner

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_organization(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        organization = _parse_organization(d.pop("organization", UNSET))

        def _parse_admin_email(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        admin_email = _parse_admin_email(d.pop("adminEmail", UNSET))

        def _parse_admin_password(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        admin_password = _parse_admin_password(d.pop("adminPassword", UNSET))

        def _parse_admin_first_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        admin_first_name = _parse_admin_first_name(d.pop("adminFirstName", UNSET))

        def _parse_admin_last_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        admin_last_name = _parse_admin_last_name(d.pop("adminLastName", UNSET))

        def _parse_frontend_theme(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        frontend_theme = _parse_frontend_theme(d.pop("frontendTheme", UNSET))

        def _parse_delegated_access_partner(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        delegated_access_partner = _parse_delegated_access_partner(d.pop("delegatedAccessPartner", UNSET))

        tenant_registration_info_dto = cls(
            organization=organization,
            admin_email=admin_email,
            admin_password=admin_password,
            admin_first_name=admin_first_name,
            admin_last_name=admin_last_name,
            frontend_theme=frontend_theme,
            delegated_access_partner=delegated_access_partner,
        )

        return tenant_registration_info_dto
