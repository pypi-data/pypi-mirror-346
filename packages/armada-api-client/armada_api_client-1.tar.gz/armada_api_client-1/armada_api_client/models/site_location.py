from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SiteLocation")


@_attrs_define
class SiteLocation:
    """
    Attributes:
        id (str):
        location_id (int):
        loc_type (int):
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
    """

    id: str
    location_id: int
    loc_type: int
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

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        loc_type = self.loc_type

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

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "locationId": location_id,
                "locType": loc_type,
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
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("locationId")

        loc_type = d.pop("locType")

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

        site_location = cls(
            id=id,
            location_id=location_id,
            loc_type=loc_type,
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
        )

        return site_location
