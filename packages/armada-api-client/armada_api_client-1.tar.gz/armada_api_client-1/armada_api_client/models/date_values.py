import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="DateValues")


@_attrs_define
class DateValues:
    """
    Attributes:
        t (datetime.datetime):
        v (Union[None, list[float]]):
    """

    t: datetime.datetime
    v: Union[None, list[float]]

    def to_dict(self) -> dict[str, Any]:
        t = self.t.isoformat()

        v: Union[None, list[float]]
        if isinstance(self.v, list):
            v = self.v

        else:
            v = self.v

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "t": t,
                "v": v,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        t = isoparse(d.pop("t"))

        def _parse_v(data: object) -> Union[None, list[float]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                v_type_0 = cast(list[float], data)

                return v_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[float]], data)

        v = _parse_v(d.pop("v"))

        date_values = cls(
            t=t,
            v=v,
        )

        return date_values
