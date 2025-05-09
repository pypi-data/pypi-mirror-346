import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_date_and_user import AuditDateAndUser


T = TypeVar("T", bound="JobHttpGet")


@_attrs_define
class JobHttpGet:
    """
    Attributes:
        id (str):
        job_id (int):
        requested_execution_date (datetime.datetime):
        first_execution_date (Union[None, datetime.datetime]):
        executed_date (Union[None, datetime.datetime]):
        process_time_ms (int):
        status (Union[None, str]):
        retry_counter (int):
        monitoring_id (int):
        relative_url (Union[None, str]):
        job_http_get_config_id (int):
        processor (Union[None, str]):
        audit (Union['AuditDateAndUser', None, Unset]):
        download_time_ms (Union[Unset, int]):
    """

    id: str
    job_id: int
    requested_execution_date: datetime.datetime
    first_execution_date: Union[None, datetime.datetime]
    executed_date: Union[None, datetime.datetime]
    process_time_ms: int
    status: Union[None, str]
    retry_counter: int
    monitoring_id: int
    relative_url: Union[None, str]
    job_http_get_config_id: int
    processor: Union[None, str]
    audit: Union["AuditDateAndUser", None, Unset] = UNSET
    download_time_ms: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_date_and_user import AuditDateAndUser

        id = self.id

        job_id = self.job_id

        requested_execution_date = self.requested_execution_date.isoformat()

        first_execution_date: Union[None, str]
        if isinstance(self.first_execution_date, datetime.datetime):
            first_execution_date = self.first_execution_date.isoformat()
        else:
            first_execution_date = self.first_execution_date

        executed_date: Union[None, str]
        if isinstance(self.executed_date, datetime.datetime):
            executed_date = self.executed_date.isoformat()
        else:
            executed_date = self.executed_date

        process_time_ms = self.process_time_ms

        status: Union[None, str]
        status = self.status

        retry_counter = self.retry_counter

        monitoring_id = self.monitoring_id

        relative_url: Union[None, str]
        relative_url = self.relative_url

        job_http_get_config_id = self.job_http_get_config_id

        processor: Union[None, str]
        processor = self.processor

        audit: Union[None, Unset, dict[str, Any]]
        if isinstance(self.audit, Unset):
            audit = UNSET
        elif isinstance(self.audit, AuditDateAndUser):
            audit = self.audit.to_dict()
        else:
            audit = self.audit

        download_time_ms = self.download_time_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "jobId": job_id,
                "requestedExecutionDate": requested_execution_date,
                "firstExecutionDate": first_execution_date,
                "executedDate": executed_date,
                "processTimeMs": process_time_ms,
                "status": status,
                "retryCounter": retry_counter,
                "monitoringId": monitoring_id,
                "relativeUrl": relative_url,
                "jobHttpGetConfigId": job_http_get_config_id,
                "processor": processor,
            }
        )
        if audit is not UNSET:
            field_dict["audit"] = audit
        if download_time_ms is not UNSET:
            field_dict["downloadTimeMs"] = download_time_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_date_and_user import AuditDateAndUser

        d = dict(src_dict)
        id = d.pop("id")

        job_id = d.pop("jobId")

        requested_execution_date = isoparse(d.pop("requestedExecutionDate"))

        def _parse_first_execution_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_execution_date_type_0 = isoparse(data)

                return first_execution_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        first_execution_date = _parse_first_execution_date(d.pop("firstExecutionDate"))

        def _parse_executed_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                executed_date_type_0 = isoparse(data)

                return executed_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        executed_date = _parse_executed_date(d.pop("executedDate"))

        process_time_ms = d.pop("processTimeMs")

        def _parse_status(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        status = _parse_status(d.pop("status"))

        retry_counter = d.pop("retryCounter")

        monitoring_id = d.pop("monitoringId")

        def _parse_relative_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        relative_url = _parse_relative_url(d.pop("relativeUrl"))

        job_http_get_config_id = d.pop("jobHttpGetConfigId")

        def _parse_processor(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        processor = _parse_processor(d.pop("processor"))

        def _parse_audit(data: object) -> Union["AuditDateAndUser", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                audit_type_1 = AuditDateAndUser.from_dict(data)

                return audit_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AuditDateAndUser", None, Unset], data)

        audit = _parse_audit(d.pop("audit", UNSET))

        download_time_ms = d.pop("downloadTimeMs", UNSET)

        job_http_get = cls(
            id=id,
            job_id=job_id,
            requested_execution_date=requested_execution_date,
            first_execution_date=first_execution_date,
            executed_date=executed_date,
            process_time_ms=process_time_ms,
            status=status,
            retry_counter=retry_counter,
            monitoring_id=monitoring_id,
            relative_url=relative_url,
            job_http_get_config_id=job_http_get_config_id,
            processor=processor,
            audit=audit,
            download_time_ms=download_time_ms,
        )

        return job_http_get
