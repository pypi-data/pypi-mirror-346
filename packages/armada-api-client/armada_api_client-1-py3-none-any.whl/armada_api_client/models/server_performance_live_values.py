from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ServerPerformanceLiveValues")


@_attrs_define
class ServerPerformanceLiveValues:
    """
    Attributes:
        cpu_usage (float):
        memory_usage (float):
        network_up_kbps (float):
        network_down_kbps (float):
    """

    cpu_usage: float
    memory_usage: float
    network_up_kbps: float
    network_down_kbps: float

    def to_dict(self) -> dict[str, Any]:
        cpu_usage = self.cpu_usage

        memory_usage = self.memory_usage

        network_up_kbps = self.network_up_kbps

        network_down_kbps = self.network_down_kbps

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "cpuUsage": cpu_usage,
                "memoryUsage": memory_usage,
                "networkUpKbps": network_up_kbps,
                "networkDownKbps": network_down_kbps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cpu_usage = d.pop("cpuUsage")

        memory_usage = d.pop("memoryUsage")

        network_up_kbps = d.pop("networkUpKbps")

        network_down_kbps = d.pop("networkDownKbps")

        server_performance_live_values = cls(
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            network_up_kbps=network_up_kbps,
            network_down_kbps=network_down_kbps,
        )

        return server_performance_live_values
