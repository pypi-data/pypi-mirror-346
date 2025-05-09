import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.alarm_element import AlarmElement
    from ..models.audit_date import AuditDate
    from ..models.configuration_element import ConfigurationElement
    from ..models.control_element import ControlElement
    from ..models.data_element import DataElement
    from ..models.description_element import DescriptionElement
    from ..models.event_element import EventElement
    from ..models.monitoring import Monitoring
    from ..models.site_location import SiteLocation


T = TypeVar("T", bound="Equipment")


@_attrs_define
class Equipment:
    """
    Attributes:
        id (str):
        equ_id (int):
        location_id (int):
        parent_id (Union[None, int]):
        monitoring_id (int):
        path (str):
        path_friendly (str):
        path_rel (str):
        path_no_id (str):
        type_ (str):
        last_update (datetime.datetime):
        last_update_description (Union[None, datetime.datetime]):
        last_update_alarm (Union[None, datetime.datetime]):
        last_update_event (Union[None, datetime.datetime]):
        last_update_data (Union[None, datetime.datetime]):
        last_update_data_record (Union[None, datetime.datetime]):
        last_update_config (Union[None, datetime.datetime]):
        last_update_control (Union[None, datetime.datetime]):
        status (str):
        severity_type (str):
        severity_level (int):
        description (str):
        reference (str):
        audit (Union['AuditDate', None, Unset]):
        maintenance_start_date (Union[None, Unset, datetime.datetime]):
        maintenance_end_date (Union[None, Unset, datetime.datetime]):
        schematic_url (Union[None, Unset, str]):
        description_elements (Union[None, Unset, list['DescriptionElement']]):
        alarm_elements (Union[None, Unset, list['AlarmElement']]):
        event_elements (Union[None, Unset, list['EventElement']]):
        data_elements (Union[None, Unset, list['DataElement']]):
        configuration_elements (Union[None, Unset, list['ConfigurationElement']]):
        control_elements (Union[None, Unset, list['ControlElement']]):
        location (Union['SiteLocation', None, Unset]):
        equ_location (Union['SiteLocation', None, Unset]):
        monitoring_status (Union[None, Unset, str]):
        monitoring (Union['Monitoring', None, Unset]):
    """

    id: str
    equ_id: int
    location_id: int
    parent_id: Union[None, int]
    monitoring_id: int
    path: str
    path_friendly: str
    path_rel: str
    path_no_id: str
    type_: str
    last_update: datetime.datetime
    last_update_description: Union[None, datetime.datetime]
    last_update_alarm: Union[None, datetime.datetime]
    last_update_event: Union[None, datetime.datetime]
    last_update_data: Union[None, datetime.datetime]
    last_update_data_record: Union[None, datetime.datetime]
    last_update_config: Union[None, datetime.datetime]
    last_update_control: Union[None, datetime.datetime]
    status: str
    severity_type: str
    severity_level: int
    description: str
    reference: str
    audit: Union["AuditDate", None, Unset] = UNSET
    maintenance_start_date: Union[None, Unset, datetime.datetime] = UNSET
    maintenance_end_date: Union[None, Unset, datetime.datetime] = UNSET
    schematic_url: Union[None, Unset, str] = UNSET
    description_elements: Union[None, Unset, list["DescriptionElement"]] = UNSET
    alarm_elements: Union[None, Unset, list["AlarmElement"]] = UNSET
    event_elements: Union[None, Unset, list["EventElement"]] = UNSET
    data_elements: Union[None, Unset, list["DataElement"]] = UNSET
    configuration_elements: Union[None, Unset, list["ConfigurationElement"]] = UNSET
    control_elements: Union[None, Unset, list["ControlElement"]] = UNSET
    location: Union["SiteLocation", None, Unset] = UNSET
    equ_location: Union["SiteLocation", None, Unset] = UNSET
    monitoring_status: Union[None, Unset, str] = UNSET
    monitoring: Union["Monitoring", None, Unset] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_date import AuditDate
        from ..models.monitoring import Monitoring
        from ..models.site_location import SiteLocation

        id = self.id

        equ_id = self.equ_id

        location_id = self.location_id

        parent_id: Union[None, int]
        parent_id = self.parent_id

        monitoring_id = self.monitoring_id

        path = self.path

        path_friendly = self.path_friendly

        path_rel = self.path_rel

        path_no_id = self.path_no_id

        type_ = self.type_

        last_update = self.last_update.isoformat()

        last_update_description: Union[None, str]
        if isinstance(self.last_update_description, datetime.datetime):
            last_update_description = self.last_update_description.isoformat()
        else:
            last_update_description = self.last_update_description

        last_update_alarm: Union[None, str]
        if isinstance(self.last_update_alarm, datetime.datetime):
            last_update_alarm = self.last_update_alarm.isoformat()
        else:
            last_update_alarm = self.last_update_alarm

        last_update_event: Union[None, str]
        if isinstance(self.last_update_event, datetime.datetime):
            last_update_event = self.last_update_event.isoformat()
        else:
            last_update_event = self.last_update_event

        last_update_data: Union[None, str]
        if isinstance(self.last_update_data, datetime.datetime):
            last_update_data = self.last_update_data.isoformat()
        else:
            last_update_data = self.last_update_data

        last_update_data_record: Union[None, str]
        if isinstance(self.last_update_data_record, datetime.datetime):
            last_update_data_record = self.last_update_data_record.isoformat()
        else:
            last_update_data_record = self.last_update_data_record

        last_update_config: Union[None, str]
        if isinstance(self.last_update_config, datetime.datetime):
            last_update_config = self.last_update_config.isoformat()
        else:
            last_update_config = self.last_update_config

        last_update_control: Union[None, str]
        if isinstance(self.last_update_control, datetime.datetime):
            last_update_control = self.last_update_control.isoformat()
        else:
            last_update_control = self.last_update_control

        status = self.status

        severity_type = self.severity_type

        severity_level = self.severity_level

        description = self.description

        reference = self.reference

        audit: Union[None, Unset, dict[str, Any]]
        if isinstance(self.audit, Unset):
            audit = UNSET
        elif isinstance(self.audit, AuditDate):
            audit = self.audit.to_dict()
        else:
            audit = self.audit

        maintenance_start_date: Union[None, Unset, str]
        if isinstance(self.maintenance_start_date, Unset):
            maintenance_start_date = UNSET
        elif isinstance(self.maintenance_start_date, datetime.datetime):
            maintenance_start_date = self.maintenance_start_date.isoformat()
        else:
            maintenance_start_date = self.maintenance_start_date

        maintenance_end_date: Union[None, Unset, str]
        if isinstance(self.maintenance_end_date, Unset):
            maintenance_end_date = UNSET
        elif isinstance(self.maintenance_end_date, datetime.datetime):
            maintenance_end_date = self.maintenance_end_date.isoformat()
        else:
            maintenance_end_date = self.maintenance_end_date

        schematic_url: Union[None, Unset, str]
        if isinstance(self.schematic_url, Unset):
            schematic_url = UNSET
        else:
            schematic_url = self.schematic_url

        description_elements: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.description_elements, Unset):
            description_elements = UNSET
        elif isinstance(self.description_elements, list):
            description_elements = []
            for description_elements_type_0_item_data in self.description_elements:
                description_elements_type_0_item = description_elements_type_0_item_data.to_dict()
                description_elements.append(description_elements_type_0_item)

        else:
            description_elements = self.description_elements

        alarm_elements: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.alarm_elements, Unset):
            alarm_elements = UNSET
        elif isinstance(self.alarm_elements, list):
            alarm_elements = []
            for alarm_elements_type_0_item_data in self.alarm_elements:
                alarm_elements_type_0_item = alarm_elements_type_0_item_data.to_dict()
                alarm_elements.append(alarm_elements_type_0_item)

        else:
            alarm_elements = self.alarm_elements

        event_elements: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.event_elements, Unset):
            event_elements = UNSET
        elif isinstance(self.event_elements, list):
            event_elements = []
            for event_elements_type_0_item_data in self.event_elements:
                event_elements_type_0_item = event_elements_type_0_item_data.to_dict()
                event_elements.append(event_elements_type_0_item)

        else:
            event_elements = self.event_elements

        data_elements: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.data_elements, Unset):
            data_elements = UNSET
        elif isinstance(self.data_elements, list):
            data_elements = []
            for data_elements_type_0_item_data in self.data_elements:
                data_elements_type_0_item = data_elements_type_0_item_data.to_dict()
                data_elements.append(data_elements_type_0_item)

        else:
            data_elements = self.data_elements

        configuration_elements: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.configuration_elements, Unset):
            configuration_elements = UNSET
        elif isinstance(self.configuration_elements, list):
            configuration_elements = []
            for configuration_elements_type_0_item_data in self.configuration_elements:
                configuration_elements_type_0_item = configuration_elements_type_0_item_data.to_dict()
                configuration_elements.append(configuration_elements_type_0_item)

        else:
            configuration_elements = self.configuration_elements

        control_elements: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.control_elements, Unset):
            control_elements = UNSET
        elif isinstance(self.control_elements, list):
            control_elements = []
            for control_elements_type_0_item_data in self.control_elements:
                control_elements_type_0_item = control_elements_type_0_item_data.to_dict()
                control_elements.append(control_elements_type_0_item)

        else:
            control_elements = self.control_elements

        location: Union[None, Unset, dict[str, Any]]
        if isinstance(self.location, Unset):
            location = UNSET
        elif isinstance(self.location, SiteLocation):
            location = self.location.to_dict()
        else:
            location = self.location

        equ_location: Union[None, Unset, dict[str, Any]]
        if isinstance(self.equ_location, Unset):
            equ_location = UNSET
        elif isinstance(self.equ_location, SiteLocation):
            equ_location = self.equ_location.to_dict()
        else:
            equ_location = self.equ_location

        monitoring_status: Union[None, Unset, str]
        if isinstance(self.monitoring_status, Unset):
            monitoring_status = UNSET
        else:
            monitoring_status = self.monitoring_status

        monitoring: Union[None, Unset, dict[str, Any]]
        if isinstance(self.monitoring, Unset):
            monitoring = UNSET
        elif isinstance(self.monitoring, Monitoring):
            monitoring = self.monitoring.to_dict()
        else:
            monitoring = self.monitoring

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "equId": equ_id,
                "locationId": location_id,
                "parentId": parent_id,
                "monitoringId": monitoring_id,
                "path": path,
                "pathFriendly": path_friendly,
                "pathRel": path_rel,
                "pathNoId": path_no_id,
                "type": type_,
                "lastUpdate": last_update,
                "lastUpdateDescription": last_update_description,
                "lastUpdateAlarm": last_update_alarm,
                "lastUpdateEvent": last_update_event,
                "lastUpdateData": last_update_data,
                "lastUpdateDataRecord": last_update_data_record,
                "lastUpdateConfig": last_update_config,
                "lastUpdateControl": last_update_control,
                "status": status,
                "severityType": severity_type,
                "severityLevel": severity_level,
                "description": description,
                "reference": reference,
            }
        )
        if audit is not UNSET:
            field_dict["audit"] = audit
        if maintenance_start_date is not UNSET:
            field_dict["maintenanceStartDate"] = maintenance_start_date
        if maintenance_end_date is not UNSET:
            field_dict["maintenanceEndDate"] = maintenance_end_date
        if schematic_url is not UNSET:
            field_dict["schematicUrl"] = schematic_url
        if description_elements is not UNSET:
            field_dict["descriptionElements"] = description_elements
        if alarm_elements is not UNSET:
            field_dict["alarmElements"] = alarm_elements
        if event_elements is not UNSET:
            field_dict["eventElements"] = event_elements
        if data_elements is not UNSET:
            field_dict["dataElements"] = data_elements
        if configuration_elements is not UNSET:
            field_dict["configurationElements"] = configuration_elements
        if control_elements is not UNSET:
            field_dict["controlElements"] = control_elements
        if location is not UNSET:
            field_dict["location"] = location
        if equ_location is not UNSET:
            field_dict["equLocation"] = equ_location
        if monitoring_status is not UNSET:
            field_dict["monitoringStatus"] = monitoring_status
        if monitoring is not UNSET:
            field_dict["monitoring"] = monitoring

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.alarm_element import AlarmElement
        from ..models.audit_date import AuditDate
        from ..models.configuration_element import ConfigurationElement
        from ..models.control_element import ControlElement
        from ..models.data_element import DataElement
        from ..models.description_element import DescriptionElement
        from ..models.event_element import EventElement
        from ..models.monitoring import Monitoring
        from ..models.site_location import SiteLocation

        d = dict(src_dict)
        id = d.pop("id")

        equ_id = d.pop("equId")

        location_id = d.pop("locationId")

        def _parse_parent_id(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        parent_id = _parse_parent_id(d.pop("parentId"))

        monitoring_id = d.pop("monitoringId")

        path = d.pop("path")

        path_friendly = d.pop("pathFriendly")

        path_rel = d.pop("pathRel")

        path_no_id = d.pop("pathNoId")

        type_ = d.pop("type")

        last_update = isoparse(d.pop("lastUpdate"))

        def _parse_last_update_description(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_description_type_0 = isoparse(data)

                return last_update_description_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_update_description = _parse_last_update_description(d.pop("lastUpdateDescription"))

        def _parse_last_update_alarm(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_alarm_type_0 = isoparse(data)

                return last_update_alarm_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_update_alarm = _parse_last_update_alarm(d.pop("lastUpdateAlarm"))

        def _parse_last_update_event(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_event_type_0 = isoparse(data)

                return last_update_event_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_update_event = _parse_last_update_event(d.pop("lastUpdateEvent"))

        def _parse_last_update_data(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_data_type_0 = isoparse(data)

                return last_update_data_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_update_data = _parse_last_update_data(d.pop("lastUpdateData"))

        def _parse_last_update_data_record(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_data_record_type_0 = isoparse(data)

                return last_update_data_record_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_update_data_record = _parse_last_update_data_record(d.pop("lastUpdateDataRecord"))

        def _parse_last_update_config(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_config_type_0 = isoparse(data)

                return last_update_config_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_update_config = _parse_last_update_config(d.pop("lastUpdateConfig"))

        def _parse_last_update_control(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_control_type_0 = isoparse(data)

                return last_update_control_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_update_control = _parse_last_update_control(d.pop("lastUpdateControl"))

        status = d.pop("status")

        severity_type = d.pop("severityType")

        severity_level = d.pop("severityLevel")

        description = d.pop("description")

        reference = d.pop("reference")

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

        def _parse_maintenance_start_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                maintenance_start_date_type_0 = isoparse(data)

                return maintenance_start_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        maintenance_start_date = _parse_maintenance_start_date(d.pop("maintenanceStartDate", UNSET))

        def _parse_maintenance_end_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                maintenance_end_date_type_0 = isoparse(data)

                return maintenance_end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        maintenance_end_date = _parse_maintenance_end_date(d.pop("maintenanceEndDate", UNSET))

        def _parse_schematic_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        schematic_url = _parse_schematic_url(d.pop("schematicUrl", UNSET))

        def _parse_description_elements(data: object) -> Union[None, Unset, list["DescriptionElement"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                description_elements_type_0 = []
                _description_elements_type_0 = data
                for description_elements_type_0_item_data in _description_elements_type_0:
                    description_elements_type_0_item = DescriptionElement.from_dict(
                        description_elements_type_0_item_data
                    )

                    description_elements_type_0.append(description_elements_type_0_item)

                return description_elements_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["DescriptionElement"]], data)

        description_elements = _parse_description_elements(d.pop("descriptionElements", UNSET))

        def _parse_alarm_elements(data: object) -> Union[None, Unset, list["AlarmElement"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                alarm_elements_type_0 = []
                _alarm_elements_type_0 = data
                for alarm_elements_type_0_item_data in _alarm_elements_type_0:
                    alarm_elements_type_0_item = AlarmElement.from_dict(alarm_elements_type_0_item_data)

                    alarm_elements_type_0.append(alarm_elements_type_0_item)

                return alarm_elements_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["AlarmElement"]], data)

        alarm_elements = _parse_alarm_elements(d.pop("alarmElements", UNSET))

        def _parse_event_elements(data: object) -> Union[None, Unset, list["EventElement"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                event_elements_type_0 = []
                _event_elements_type_0 = data
                for event_elements_type_0_item_data in _event_elements_type_0:
                    event_elements_type_0_item = EventElement.from_dict(event_elements_type_0_item_data)

                    event_elements_type_0.append(event_elements_type_0_item)

                return event_elements_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["EventElement"]], data)

        event_elements = _parse_event_elements(d.pop("eventElements", UNSET))

        def _parse_data_elements(data: object) -> Union[None, Unset, list["DataElement"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                data_elements_type_0 = []
                _data_elements_type_0 = data
                for data_elements_type_0_item_data in _data_elements_type_0:
                    data_elements_type_0_item = DataElement.from_dict(data_elements_type_0_item_data)

                    data_elements_type_0.append(data_elements_type_0_item)

                return data_elements_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["DataElement"]], data)

        data_elements = _parse_data_elements(d.pop("dataElements", UNSET))

        def _parse_configuration_elements(data: object) -> Union[None, Unset, list["ConfigurationElement"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                configuration_elements_type_0 = []
                _configuration_elements_type_0 = data
                for configuration_elements_type_0_item_data in _configuration_elements_type_0:
                    configuration_elements_type_0_item = ConfigurationElement.from_dict(
                        configuration_elements_type_0_item_data
                    )

                    configuration_elements_type_0.append(configuration_elements_type_0_item)

                return configuration_elements_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["ConfigurationElement"]], data)

        configuration_elements = _parse_configuration_elements(d.pop("configurationElements", UNSET))

        def _parse_control_elements(data: object) -> Union[None, Unset, list["ControlElement"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                control_elements_type_0 = []
                _control_elements_type_0 = data
                for control_elements_type_0_item_data in _control_elements_type_0:
                    control_elements_type_0_item = ControlElement.from_dict(control_elements_type_0_item_data)

                    control_elements_type_0.append(control_elements_type_0_item)

                return control_elements_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["ControlElement"]], data)

        control_elements = _parse_control_elements(d.pop("controlElements", UNSET))

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

        def _parse_equ_location(data: object) -> Union["SiteLocation", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                equ_location_type_1 = SiteLocation.from_dict(data)

                return equ_location_type_1
            except:  # noqa: E722
                pass
            return cast(Union["SiteLocation", None, Unset], data)

        equ_location = _parse_equ_location(d.pop("equLocation", UNSET))

        def _parse_monitoring_status(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        monitoring_status = _parse_monitoring_status(d.pop("monitoringStatus", UNSET))

        def _parse_monitoring(data: object) -> Union["Monitoring", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                monitoring_type_1 = Monitoring.from_dict(data)

                return monitoring_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Monitoring", None, Unset], data)

        monitoring = _parse_monitoring(d.pop("monitoring", UNSET))

        equipment = cls(
            id=id,
            equ_id=equ_id,
            location_id=location_id,
            parent_id=parent_id,
            monitoring_id=monitoring_id,
            path=path,
            path_friendly=path_friendly,
            path_rel=path_rel,
            path_no_id=path_no_id,
            type_=type_,
            last_update=last_update,
            last_update_description=last_update_description,
            last_update_alarm=last_update_alarm,
            last_update_event=last_update_event,
            last_update_data=last_update_data,
            last_update_data_record=last_update_data_record,
            last_update_config=last_update_config,
            last_update_control=last_update_control,
            status=status,
            severity_type=severity_type,
            severity_level=severity_level,
            description=description,
            reference=reference,
            audit=audit,
            maintenance_start_date=maintenance_start_date,
            maintenance_end_date=maintenance_end_date,
            schematic_url=schematic_url,
            description_elements=description_elements,
            alarm_elements=alarm_elements,
            event_elements=event_elements,
            data_elements=data_elements,
            configuration_elements=configuration_elements,
            control_elements=control_elements,
            location=location,
            equ_location=equ_location,
            monitoring_status=monitoring_status,
            monitoring=monitoring,
        )

        return equipment
