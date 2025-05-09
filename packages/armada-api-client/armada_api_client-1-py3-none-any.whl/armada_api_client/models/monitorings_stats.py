from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MonitoringsStats")


@_attrs_define
class MonitoringsStats:
    """
    Attributes:
        count (int):
        online (int):
    """

    count: int
    online: int

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        online = self.online

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "count": count,
                "online": online,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        online = d.pop("online")

        monitorings_stats = cls(
            count=count,
            online=online,
        )

        return monitorings_stats
