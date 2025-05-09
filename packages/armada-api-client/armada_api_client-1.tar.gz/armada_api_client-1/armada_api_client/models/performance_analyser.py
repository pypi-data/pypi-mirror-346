from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PerformanceAnalyser")


@_attrs_define
class PerformanceAnalyser:
    """
    Attributes:
        id (int):
        name (str):
        unit (str):
    """

    id: int
    name: str
    unit: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        unit = d.pop("unit")

        performance_analyser = cls(
            id=id,
            name=name,
            unit=unit,
        )

        return performance_analyser
