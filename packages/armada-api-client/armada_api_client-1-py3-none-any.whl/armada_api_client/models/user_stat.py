import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="UserStat")


@_attrs_define
class UserStat:
    """
    Attributes:
        login (Union[None, str]):
        last_request_dt (Union[None, datetime.datetime]):
    """

    login: Union[None, str]
    last_request_dt: Union[None, datetime.datetime]

    def to_dict(self) -> dict[str, Any]:
        login: Union[None, str]
        login = self.login

        last_request_dt: Union[None, str]
        if isinstance(self.last_request_dt, datetime.datetime):
            last_request_dt = self.last_request_dt.isoformat()
        else:
            last_request_dt = self.last_request_dt

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "login": login,
                "lastRequestDt": last_request_dt,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_login(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        login = _parse_login(d.pop("login"))

        def _parse_last_request_dt(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_request_dt_type_0 = isoparse(data)

                return last_request_dt_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_request_dt = _parse_last_request_dt(d.pop("lastRequestDt"))

        user_stat = cls(
            login=login,
            last_request_dt=last_request_dt,
        )

        return user_stat
