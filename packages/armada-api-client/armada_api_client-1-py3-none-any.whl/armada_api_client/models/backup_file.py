import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="BackupFile")


@_attrs_define
class BackupFile:
    """
    Attributes:
        monitoring_id (int):
        file_name (str):
        backup_datetime (datetime.datetime):
    """

    monitoring_id: int
    file_name: str
    backup_datetime: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        monitoring_id = self.monitoring_id

        file_name = self.file_name

        backup_datetime = self.backup_datetime.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "monitoringId": monitoring_id,
                "fileName": file_name,
                "backupDatetime": backup_datetime,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        monitoring_id = d.pop("monitoringId")

        file_name = d.pop("fileName")

        backup_datetime = isoparse(d.pop("backupDatetime"))

        backup_file = cls(
            monitoring_id=monitoring_id,
            file_name=file_name,
            backup_datetime=backup_datetime,
        )

        return backup_file
