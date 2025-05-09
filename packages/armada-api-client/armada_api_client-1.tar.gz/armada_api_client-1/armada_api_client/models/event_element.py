import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_date import AuditDate
    from ..models.equipment import Equipment


T = TypeVar("T", bound="EventElement")


@_attrs_define
class EventElement:
    """
    Attributes:
        equ_id (int):
        name (str):
        group (str):
        sub_group (str):
        id (str):
        alarm_id (int):
        event_id (int):
        severity_type (str):
        severity_level (int):
        date_time (datetime.datetime):
        event_type (str):
        audit (Union['AuditDate', None, Unset]):
        equipment (Union['Equipment', None, Unset]):
    """

    equ_id: int
    name: str
    group: str
    sub_group: str
    id: str
    alarm_id: int
    event_id: int
    severity_type: str
    severity_level: int
    date_time: datetime.datetime
    event_type: str
    audit: Union["AuditDate", None, Unset] = UNSET
    equipment: Union["Equipment", None, Unset] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_date import AuditDate
        from ..models.equipment import Equipment

        equ_id = self.equ_id

        name = self.name

        group = self.group

        sub_group = self.sub_group

        id = self.id

        alarm_id = self.alarm_id

        event_id = self.event_id

        severity_type = self.severity_type

        severity_level = self.severity_level

        date_time = self.date_time.isoformat()

        event_type = self.event_type

        audit: Union[None, Unset, dict[str, Any]]
        if isinstance(self.audit, Unset):
            audit = UNSET
        elif isinstance(self.audit, AuditDate):
            audit = self.audit.to_dict()
        else:
            audit = self.audit

        equipment: Union[None, Unset, dict[str, Any]]
        if isinstance(self.equipment, Unset):
            equipment = UNSET
        elif isinstance(self.equipment, Equipment):
            equipment = self.equipment.to_dict()
        else:
            equipment = self.equipment

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "equId": equ_id,
                "name": name,
                "group": group,
                "subGroup": sub_group,
                "id": id,
                "alarmId": alarm_id,
                "eventId": event_id,
                "severityType": severity_type,
                "severityLevel": severity_level,
                "dateTime": date_time,
                "eventType": event_type,
            }
        )
        if audit is not UNSET:
            field_dict["audit"] = audit
        if equipment is not UNSET:
            field_dict["equipment"] = equipment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_date import AuditDate
        from ..models.equipment import Equipment

        d = dict(src_dict)
        equ_id = d.pop("equId")

        name = d.pop("name")

        group = d.pop("group")

        sub_group = d.pop("subGroup")

        id = d.pop("id")

        alarm_id = d.pop("alarmId")

        event_id = d.pop("eventId")

        severity_type = d.pop("severityType")

        severity_level = d.pop("severityLevel")

        date_time = isoparse(d.pop("dateTime"))

        event_type = d.pop("eventType")

        def _parse_audit(data: object) -> Union["AuditDate", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                audit_type_1 = AuditDate.from_dict(data)

                return audit_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AuditDate", None, Unset], data)

        audit = _parse_audit(d.pop("audit", UNSET))

        def _parse_equipment(data: object) -> Union["Equipment", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                equipment_type_1 = Equipment.from_dict(data)

                return equipment_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Equipment", None, Unset], data)

        equipment = _parse_equipment(d.pop("equipment", UNSET))

        event_element = cls(
            equ_id=equ_id,
            name=name,
            group=group,
            sub_group=sub_group,
            id=id,
            alarm_id=alarm_id,
            event_id=event_id,
            severity_type=severity_type,
            severity_level=severity_level,
            date_time=date_time,
            event_type=event_type,
            audit=audit,
            equipment=equipment,
        )

        return event_element
