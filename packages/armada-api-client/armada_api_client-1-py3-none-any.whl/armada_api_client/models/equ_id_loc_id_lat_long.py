from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="EquIdLocIdLatLong")


@_attrs_define
class EquIdLocIdLatLong:
    """
    Attributes:
        equ_id (int):
        location_id (int):
        latitude (float):
        longitude (float):
    """

    equ_id: int
    location_id: int
    latitude: float
    longitude: float

    def to_dict(self) -> dict[str, Any]:
        equ_id = self.equ_id

        location_id = self.location_id

        latitude = self.latitude

        longitude = self.longitude

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "equId": equ_id,
                "locationId": location_id,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        equ_id = d.pop("equId")

        location_id = d.pop("locationId")

        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        equ_id_loc_id_lat_long = cls(
            equ_id=equ_id,
            location_id=location_id,
            latitude=latitude,
            longitude=longitude,
        )

        return equ_id_loc_id_lat_long
