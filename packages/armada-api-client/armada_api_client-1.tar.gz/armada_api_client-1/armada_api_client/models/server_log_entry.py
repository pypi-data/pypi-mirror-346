import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="ServerLogEntry")


@_attrs_define
class ServerLogEntry:
    """
    Attributes:
        id (int):
        date (datetime.datetime):
        thread (str):
        level (str):
        logger (str):
        method (str):
        parameters (str):
        message (str):
        exception (str):
    """

    id: int
    date: datetime.datetime
    thread: str
    level: str
    logger: str
    method: str
    parameters: str
    message: str
    exception: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        date = self.date.isoformat()

        thread = self.thread

        level = self.level

        logger = self.logger

        method = self.method

        parameters = self.parameters

        message = self.message

        exception = self.exception

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "date": date,
                "thread": thread,
                "level": level,
                "logger": logger,
                "method": method,
                "parameters": parameters,
                "message": message,
                "exception": exception,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        date = isoparse(d.pop("date"))

        thread = d.pop("thread")

        level = d.pop("level")

        logger = d.pop("logger")

        method = d.pop("method")

        parameters = d.pop("parameters")

        message = d.pop("message")

        exception = d.pop("exception")

        server_log_entry = cls(
            id=id,
            date=date,
            thread=thread,
            level=level,
            logger=logger,
            method=method,
            parameters=parameters,
            message=message,
            exception=exception,
        )

        return server_log_entry
