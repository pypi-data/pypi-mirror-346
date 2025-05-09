from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_date_and_user import AuditDateAndUser
    from ..models.equipment import Equipment
    from ..models.site_location import SiteLocation


T = TypeVar("T", bound="Monitoring")


@_attrs_define
class Monitoring:
    """
    Attributes:
        id (str):
        monitoring_id (int):
        location_id (int):
        ip_address (str):
        web_login (Union[None, str]):
        web_password (Union[None, str]):
        web_login_ro (Union[None, str]):
        web_password_ro (Union[None, str]):
        web_port (int):
        ftp_login (Union[None, str]):
        ftp_password (Union[None, str]):
        ftp_port (int):
        connection_status (Union[None, str]):
        type_ (Union[None, str]):
        audit (Union['AuditDateAndUser', None, Unset]):
        location (Union['SiteLocation', None, Unset]):
        equipments (Union[None, Unset, list['Equipment']]):
    """

    id: str
    monitoring_id: int
    location_id: int
    ip_address: str
    web_login: Union[None, str]
    web_password: Union[None, str]
    web_login_ro: Union[None, str]
    web_password_ro: Union[None, str]
    web_port: int
    ftp_login: Union[None, str]
    ftp_password: Union[None, str]
    ftp_port: int
    connection_status: Union[None, str]
    type_: Union[None, str]
    audit: Union["AuditDateAndUser", None, Unset] = UNSET
    location: Union["SiteLocation", None, Unset] = UNSET
    equipments: Union[None, Unset, list["Equipment"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_date_and_user import AuditDateAndUser
        from ..models.site_location import SiteLocation

        id = self.id

        monitoring_id = self.monitoring_id

        location_id = self.location_id

        ip_address = self.ip_address

        web_login: Union[None, str]
        web_login = self.web_login

        web_password: Union[None, str]
        web_password = self.web_password

        web_login_ro: Union[None, str]
        web_login_ro = self.web_login_ro

        web_password_ro: Union[None, str]
        web_password_ro = self.web_password_ro

        web_port = self.web_port

        ftp_login: Union[None, str]
        ftp_login = self.ftp_login

        ftp_password: Union[None, str]
        ftp_password = self.ftp_password

        ftp_port = self.ftp_port

        connection_status: Union[None, str]
        connection_status = self.connection_status

        type_: Union[None, str]
        type_ = self.type_

        audit: Union[None, Unset, dict[str, Any]]
        if isinstance(self.audit, Unset):
            audit = UNSET
        elif isinstance(self.audit, AuditDateAndUser):
            audit = self.audit.to_dict()
        else:
            audit = self.audit

        location: Union[None, Unset, dict[str, Any]]
        if isinstance(self.location, Unset):
            location = UNSET
        elif isinstance(self.location, SiteLocation):
            location = self.location.to_dict()
        else:
            location = self.location

        equipments: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.equipments, Unset):
            equipments = UNSET
        elif isinstance(self.equipments, list):
            equipments = []
            for equipments_type_0_item_data in self.equipments:
                equipments_type_0_item = equipments_type_0_item_data.to_dict()
                equipments.append(equipments_type_0_item)

        else:
            equipments = self.equipments

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "monitoringId": monitoring_id,
                "locationId": location_id,
                "ipAddress": ip_address,
                "webLogin": web_login,
                "webPassword": web_password,
                "webLoginRo": web_login_ro,
                "webPasswordRo": web_password_ro,
                "webPort": web_port,
                "ftpLogin": ftp_login,
                "ftpPassword": ftp_password,
                "ftpPort": ftp_port,
                "connectionStatus": connection_status,
                "type": type_,
            }
        )
        if audit is not UNSET:
            field_dict["audit"] = audit
        if location is not UNSET:
            field_dict["location"] = location
        if equipments is not UNSET:
            field_dict["equipments"] = equipments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_date_and_user import AuditDateAndUser
        from ..models.equipment import Equipment
        from ..models.site_location import SiteLocation

        d = dict(src_dict)
        id = d.pop("id")

        monitoring_id = d.pop("monitoringId")

        location_id = d.pop("locationId")

        ip_address = d.pop("ipAddress")

        def _parse_web_login(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        web_login = _parse_web_login(d.pop("webLogin"))

        def _parse_web_password(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        web_password = _parse_web_password(d.pop("webPassword"))

        def _parse_web_login_ro(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        web_login_ro = _parse_web_login_ro(d.pop("webLoginRo"))

        def _parse_web_password_ro(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        web_password_ro = _parse_web_password_ro(d.pop("webPasswordRo"))

        web_port = d.pop("webPort")

        def _parse_ftp_login(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        ftp_login = _parse_ftp_login(d.pop("ftpLogin"))

        def _parse_ftp_password(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        ftp_password = _parse_ftp_password(d.pop("ftpPassword"))

        ftp_port = d.pop("ftpPort")

        def _parse_connection_status(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        connection_status = _parse_connection_status(d.pop("connectionStatus"))

        def _parse_type_(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        type_ = _parse_type_(d.pop("type"))

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

        def _parse_location(data: object) -> Union["SiteLocation", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_type_1 = SiteLocation.from_dict(data)

                return location_type_1
            except:  # noqa: E722
                pass
            return cast(Union["SiteLocation", None, Unset], data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_equipments(data: object) -> Union[None, Unset, list["Equipment"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                equipments_type_0 = []
                _equipments_type_0 = data
                for equipments_type_0_item_data in _equipments_type_0:
                    equipments_type_0_item = Equipment.from_dict(equipments_type_0_item_data)

                    equipments_type_0.append(equipments_type_0_item)

                return equipments_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Equipment"]], data)

        equipments = _parse_equipments(d.pop("equipments", UNSET))

        monitoring = cls(
            id=id,
            monitoring_id=monitoring_id,
            location_id=location_id,
            ip_address=ip_address,
            web_login=web_login,
            web_password=web_password,
            web_login_ro=web_login_ro,
            web_password_ro=web_password_ro,
            web_port=web_port,
            ftp_login=ftp_login,
            ftp_password=ftp_password,
            ftp_port=ftp_port,
            connection_status=connection_status,
            type_=type_,
            audit=audit,
            location=location,
            equipments=equipments,
        )

        return monitoring
