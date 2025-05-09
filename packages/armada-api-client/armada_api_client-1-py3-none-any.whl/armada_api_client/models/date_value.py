import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="DateValue")


@_attrs_define
class DateValue:
    """
    Attributes:
        t (Union[None, datetime.datetime]):
        v (Union[None, float]):
    """

    t: Union[None, datetime.datetime]
    v: Union[None, float]

    def to_dict(self) -> dict[str, Any]:
        t: Union[None, str]
        if isinstance(self.t, datetime.datetime):
            t = self.t.isoformat()
        else:
            t = self.t

        v: Union[None, float]
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

        def _parse_t(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                t_type_0 = isoparse(data)

                return t_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        t = _parse_t(d.pop("t"))

        def _parse_v(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        v = _parse_v(d.pop("v"))

        date_value = cls(
            t=t,
            v=v,
        )

        return date_value
