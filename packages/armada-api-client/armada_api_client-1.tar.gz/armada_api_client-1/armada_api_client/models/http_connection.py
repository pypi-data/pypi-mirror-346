import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpConnection")


@_attrs_define
class HttpConnection:
    """
    Attributes:
        id (str):
        login (Union[None, Unset, str]):
        ip_address (Union[None, Unset, str]):
        last_request (Union[Unset, datetime.datetime]):
        first_request (Union[Unset, datetime.datetime]):
        counter (Union[Unset, int]):
        last_path (Union[None, Unset, str]):
    """

    id: str
    login: Union[None, Unset, str] = UNSET
    ip_address: Union[None, Unset, str] = UNSET
    last_request: Union[Unset, datetime.datetime] = UNSET
    first_request: Union[Unset, datetime.datetime] = UNSET
    counter: Union[Unset, int] = UNSET
    last_path: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        login: Union[None, Unset, str]
        if isinstance(self.login, Unset):
            login = UNSET
        else:
            login = self.login

        ip_address: Union[None, Unset, str]
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        last_request: Union[Unset, str] = UNSET
        if not isinstance(self.last_request, Unset):
            last_request = self.last_request.isoformat()

        first_request: Union[Unset, str] = UNSET
        if not isinstance(self.first_request, Unset):
            first_request = self.first_request.isoformat()

        counter = self.counter

        last_path: Union[None, Unset, str]
        if isinstance(self.last_path, Unset):
            last_path = UNSET
        else:
            last_path = self.last_path

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if login is not UNSET:
            field_dict["login"] = login
        if ip_address is not UNSET:
            field_dict["ipAddress"] = ip_address
        if last_request is not UNSET:
            field_dict["lastRequest"] = last_request
        if first_request is not UNSET:
            field_dict["firstRequest"] = first_request
        if counter is not UNSET:
            field_dict["counter"] = counter
        if last_path is not UNSET:
            field_dict["lastPath"] = last_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_login(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        login = _parse_login(d.pop("login", UNSET))

        def _parse_ip_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ip_address = _parse_ip_address(d.pop("ipAddress", UNSET))

        _last_request = d.pop("lastRequest", UNSET)
        last_request: Union[Unset, datetime.datetime]
        if isinstance(_last_request, Unset):
            last_request = UNSET
        else:
            last_request = isoparse(_last_request)

        _first_request = d.pop("firstRequest", UNSET)
        first_request: Union[Unset, datetime.datetime]
        if isinstance(_first_request, Unset):
            first_request = UNSET
        else:
            first_request = isoparse(_first_request)

        counter = d.pop("counter", UNSET)

        def _parse_last_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_path = _parse_last_path(d.pop("lastPath", UNSET))

        http_connection = cls(
            id=id,
            login=login,
            ip_address=ip_address,
            last_request=last_request,
            first_request=first_request,
            counter=counter,
            last_path=last_path,
        )

        return http_connection
