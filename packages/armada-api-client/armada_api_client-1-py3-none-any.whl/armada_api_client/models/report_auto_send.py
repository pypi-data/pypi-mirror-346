import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportAutoSend")


@_attrs_define
class ReportAutoSend:
    """
    Attributes:
        report_auto_send_id (int):
        report_id (int):
        user_ids_as_csv (str):
        next_sending_datetime (datetime.datetime):
        sending_condition (str):
        sending_method (str):
        cron_string (str):
        last_sent_datetime (datetime.datetime):
        id (Union[None, Unset, str]):
    """

    report_auto_send_id: int
    report_id: int
    user_ids_as_csv: str
    next_sending_datetime: datetime.datetime
    sending_condition: str
    sending_method: str
    cron_string: str
    last_sent_datetime: datetime.datetime
    id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        report_auto_send_id = self.report_auto_send_id

        report_id = self.report_id

        user_ids_as_csv = self.user_ids_as_csv

        next_sending_datetime = self.next_sending_datetime.isoformat()

        sending_condition = self.sending_condition

        sending_method = self.sending_method

        cron_string = self.cron_string

        last_sent_datetime = self.last_sent_datetime.isoformat()

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "reportAutoSendId": report_auto_send_id,
                "reportId": report_id,
                "userIdsAsCsv": user_ids_as_csv,
                "nextSendingDatetime": next_sending_datetime,
                "sendingCondition": sending_condition,
                "sendingMethod": sending_method,
                "cronString": cron_string,
                "lastSentDatetime": last_sent_datetime,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        report_auto_send_id = d.pop("reportAutoSendId")

        report_id = d.pop("reportId")

        user_ids_as_csv = d.pop("userIdsAsCsv")

        next_sending_datetime = isoparse(d.pop("nextSendingDatetime"))

        sending_condition = d.pop("sendingCondition")

        sending_method = d.pop("sendingMethod")

        cron_string = d.pop("cronString")

        last_sent_datetime = isoparse(d.pop("lastSentDatetime"))

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        report_auto_send = cls(
            report_auto_send_id=report_auto_send_id,
            report_id=report_id,
            user_ids_as_csv=user_ids_as_csv,
            next_sending_datetime=next_sending_datetime,
            sending_condition=sending_condition,
            sending_method=sending_method,
            cron_string=cron_string,
            last_sent_datetime=last_sent_datetime,
            id=id,
        )

        return report_auto_send
