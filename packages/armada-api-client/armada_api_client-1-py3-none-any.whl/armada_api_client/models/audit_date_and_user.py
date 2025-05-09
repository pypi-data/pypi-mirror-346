import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditDateAndUser")


@_attrs_define
class AuditDateAndUser:
    """
    Attributes:
        created_by (Union[None, str]):
        modified_by (Union[None, str]):
        created_date (Union[Unset, datetime.datetime]):
        modified_date (Union[None, Unset, datetime.datetime]):
    """

    created_by: Union[None, str]
    modified_by: Union[None, str]
    created_date: Union[Unset, datetime.datetime] = UNSET
    modified_date: Union[None, Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        created_by: Union[None, str]
        created_by = self.created_by

        modified_by: Union[None, str]
        modified_by = self.modified_by

        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()

        modified_date: Union[None, Unset, str]
        if isinstance(self.modified_date, Unset):
            modified_date = UNSET
        elif isinstance(self.modified_date, datetime.datetime):
            modified_date = self.modified_date.isoformat()
        else:
            modified_date = self.modified_date

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "createdBy": created_by,
                "modifiedBy": modified_by,
            }
        )
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if modified_date is not UNSET:
            field_dict["modifiedDate"] = modified_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_created_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by = _parse_created_by(d.pop("createdBy"))

        def _parse_modified_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        modified_by = _parse_modified_by(d.pop("modifiedBy"))

        _created_date = d.pop("createdDate", UNSET)
        created_date: Union[Unset, datetime.datetime]
        if isinstance(_created_date, Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date)

        def _parse_modified_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                modified_date_type_0 = isoparse(data)

                return modified_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        modified_date = _parse_modified_date(d.pop("modifiedDate", UNSET))

        audit_date_and_user = cls(
            created_by=created_by,
            modified_by=modified_by,
            created_date=created_date,
            modified_date=modified_date,
        )

        return audit_date_and_user
