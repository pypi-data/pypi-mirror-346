import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_date import AuditDate
    from ..models.equipment import Equipment


T = TypeVar("T", bound="AlarmElement")


@_attrs_define
class AlarmElement:
    """
    Attributes:
        equ_id (int):
        name (str):
        group (str):
        sub_group (str):
        id (str):
        alarm_id (int):
        active (bool):
        severity_type (str):
        severity_level (int):
        acknowledged (bool):
        clear_delay (int):
        set_delay (int):
        relay (int):
        audit (Union['AuditDate', None, Unset]):
        equipment (Union['Equipment', None, Unset]):
        start_date_time (Union[None, Unset, datetime.datetime]):
        stop_date_time (Union[None, Unset, datetime.datetime]):
        ack_date_time (Union[None, Unset, datetime.datetime]):
    """

    equ_id: int
    name: str
    group: str
    sub_group: str
    id: str
    alarm_id: int
    active: bool
    severity_type: str
    severity_level: int
    acknowledged: bool
    clear_delay: int
    set_delay: int
    relay: int
    audit: Union["AuditDate", None, Unset] = UNSET
    equipment: Union["Equipment", None, Unset] = UNSET
    start_date_time: Union[None, Unset, datetime.datetime] = UNSET
    stop_date_time: Union[None, Unset, datetime.datetime] = UNSET
    ack_date_time: Union[None, Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_date import AuditDate
        from ..models.equipment import Equipment

        equ_id = self.equ_id

        name = self.name

        group = self.group

        sub_group = self.sub_group

        id = self.id

        alarm_id = self.alarm_id

        active = self.active

        severity_type = self.severity_type

        severity_level = self.severity_level

        acknowledged = self.acknowledged

        clear_delay = self.clear_delay

        set_delay = self.set_delay

        relay = self.relay

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

        start_date_time: Union[None, Unset, str]
        if isinstance(self.start_date_time, Unset):
            start_date_time = UNSET
        elif isinstance(self.start_date_time, datetime.datetime):
            start_date_time = self.start_date_time.isoformat()
        else:
            start_date_time = self.start_date_time

        stop_date_time: Union[None, Unset, str]
        if isinstance(self.stop_date_time, Unset):
            stop_date_time = UNSET
        elif isinstance(self.stop_date_time, datetime.datetime):
            stop_date_time = self.stop_date_time.isoformat()
        else:
            stop_date_time = self.stop_date_time

        ack_date_time: Union[None, Unset, str]
        if isinstance(self.ack_date_time, Unset):
            ack_date_time = UNSET
        elif isinstance(self.ack_date_time, datetime.datetime):
            ack_date_time = self.ack_date_time.isoformat()
        else:
            ack_date_time = self.ack_date_time

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "equId": equ_id,
                "name": name,
                "group": group,
                "subGroup": sub_group,
                "id": id,
                "alarmId": alarm_id,
                "active": active,
                "severityType": severity_type,
                "severityLevel": severity_level,
                "acknowledged": acknowledged,
                "clearDelay": clear_delay,
                "setDelay": set_delay,
                "relay": relay,
            }
        )
        if audit is not UNSET:
            field_dict["audit"] = audit
        if equipment is not UNSET:
            field_dict["equipment"] = equipment
        if start_date_time is not UNSET:
            field_dict["startDateTime"] = start_date_time
        if stop_date_time is not UNSET:
            field_dict["stopDateTime"] = stop_date_time
        if ack_date_time is not UNSET:
            field_dict["ackDateTime"] = ack_date_time

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

        active = d.pop("active")

        severity_type = d.pop("severityType")

        severity_level = d.pop("severityLevel")

        acknowledged = d.pop("acknowledged")

        clear_delay = d.pop("clearDelay")

        set_delay = d.pop("setDelay")

        relay = d.pop("relay")

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

        def _parse_start_date_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_time_type_0 = isoparse(data)

                return start_date_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start_date_time = _parse_start_date_time(d.pop("startDateTime", UNSET))

        def _parse_stop_date_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                stop_date_time_type_0 = isoparse(data)

                return stop_date_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        stop_date_time = _parse_stop_date_time(d.pop("stopDateTime", UNSET))

        def _parse_ack_date_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ack_date_time_type_0 = isoparse(data)

                return ack_date_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        ack_date_time = _parse_ack_date_time(d.pop("ackDateTime", UNSET))

        alarm_element = cls(
            equ_id=equ_id,
            name=name,
            group=group,
            sub_group=sub_group,
            id=id,
            alarm_id=alarm_id,
            active=active,
            severity_type=severity_type,
            severity_level=severity_level,
            acknowledged=acknowledged,
            clear_delay=clear_delay,
            set_delay=set_delay,
            relay=relay,
            audit=audit,
            equipment=equipment,
            start_date_time=start_date_time,
            stop_date_time=stop_date_time,
            ack_date_time=ack_date_time,
        )

        return alarm_element
