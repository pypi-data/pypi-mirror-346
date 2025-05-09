import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="MonitoringSiteLocation")


@_attrs_define
class MonitoringSiteLocation:
    """
    Attributes:
        id (str):
        location_id (int):
        monitoring_id (int):
        name (str):
        info (str):
        country (str):
        region (str):
        province (str):
        city (str):
        type_ (str):
        group1 (str):
        group2 (str):
        group3 (str):
        group4 (str):
        group5 (str):
        latitude (float):
        longitude (float):
        connection_status (str):
        alarm_severity_type (str):
        status (str):
        ip_address (str):
        created (datetime.datetime):
    """

    id: str
    location_id: int
    monitoring_id: int
    name: str
    info: str
    country: str
    region: str
    province: str
    city: str
    type_: str
    group1: str
    group2: str
    group3: str
    group4: str
    group5: str
    latitude: float
    longitude: float
    connection_status: str
    alarm_severity_type: str
    status: str
    ip_address: str
    created: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        monitoring_id = self.monitoring_id

        name = self.name

        info = self.info

        country = self.country

        region = self.region

        province = self.province

        city = self.city

        type_ = self.type_

        group1 = self.group1

        group2 = self.group2

        group3 = self.group3

        group4 = self.group4

        group5 = self.group5

        latitude = self.latitude

        longitude = self.longitude

        connection_status = self.connection_status

        alarm_severity_type = self.alarm_severity_type

        status = self.status

        ip_address = self.ip_address

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "locationId": location_id,
                "monitoringId": monitoring_id,
                "name": name,
                "info": info,
                "country": country,
                "region": region,
                "province": province,
                "city": city,
                "type": type_,
                "group1": group1,
                "group2": group2,
                "group3": group3,
                "group4": group4,
                "group5": group5,
                "latitude": latitude,
                "longitude": longitude,
                "connectionStatus": connection_status,
                "alarmSeverityType": alarm_severity_type,
                "status": status,
                "ipAddress": ip_address,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("locationId")

        monitoring_id = d.pop("monitoringId")

        name = d.pop("name")

        info = d.pop("info")

        country = d.pop("country")

        region = d.pop("region")

        province = d.pop("province")

        city = d.pop("city")

        type_ = d.pop("type")

        group1 = d.pop("group1")

        group2 = d.pop("group2")

        group3 = d.pop("group3")

        group4 = d.pop("group4")

        group5 = d.pop("group5")

        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        connection_status = d.pop("connectionStatus")

        alarm_severity_type = d.pop("alarmSeverityType")

        status = d.pop("status")

        ip_address = d.pop("ipAddress")

        created = isoparse(d.pop("created"))

        monitoring_site_location = cls(
            id=id,
            location_id=location_id,
            monitoring_id=monitoring_id,
            name=name,
            info=info,
            country=country,
            region=region,
            province=province,
            city=city,
            type_=type_,
            group1=group1,
            group2=group2,
            group3=group3,
            group4=group4,
            group5=group5,
            latitude=latitude,
            longitude=longitude,
            connection_status=connection_status,
            alarm_severity_type=alarm_severity_type,
            status=status,
            ip_address=ip_address,
            created=created,
        )

        return monitoring_site_location
