import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_date_and_user import AuditDateAndUser


T = TypeVar("T", bound="JobTask")


@_attrs_define
class JobTask:
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
        name (Union[None, str]):
        param_str_1 (Union[None, str]):
        param_str_2 (Union[None, str]):
        param_str_3 (Union[None, str]):
        param_int_1 (Union[None, str]):
        param_int_2 (Union[None, str]):
        param_int_3 (Union[None, str]):
        file_info_id (int):
        task_result (Union[None, str]):
        audit (Union['AuditDateAndUser', None, Unset]):
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
    name: Union[None, str]
    param_str_1: Union[None, str]
    param_str_2: Union[None, str]
    param_str_3: Union[None, str]
    param_int_1: Union[None, str]
    param_int_2: Union[None, str]
    param_int_3: Union[None, str]
    file_info_id: int
    task_result: Union[None, str]
    audit: Union["AuditDateAndUser", None, Unset] = UNSET

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

        name: Union[None, str]
        name = self.name

        param_str_1: Union[None, str]
        param_str_1 = self.param_str_1

        param_str_2: Union[None, str]
        param_str_2 = self.param_str_2

        param_str_3: Union[None, str]
        param_str_3 = self.param_str_3

        param_int_1: Union[None, str]
        param_int_1 = self.param_int_1

        param_int_2: Union[None, str]
        param_int_2 = self.param_int_2

        param_int_3: Union[None, str]
        param_int_3 = self.param_int_3

        file_info_id = self.file_info_id

        task_result: Union[None, str]
        task_result = self.task_result

        audit: Union[None, Unset, dict[str, Any]]
        if isinstance(self.audit, Unset):
            audit = UNSET
        elif isinstance(self.audit, AuditDateAndUser):
            audit = self.audit.to_dict()
        else:
            audit = self.audit

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
                "name": name,
                "paramStr1": param_str_1,
                "paramStr2": param_str_2,
                "paramStr3": param_str_3,
                "paramInt1": param_int_1,
                "paramInt2": param_int_2,
                "paramInt3": param_int_3,
                "fileInfoId": file_info_id,
                "taskResult": task_result,
            }
        )
        if audit is not UNSET:
            field_dict["audit"] = audit

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

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        def _parse_param_str_1(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        param_str_1 = _parse_param_str_1(d.pop("paramStr1"))

        def _parse_param_str_2(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        param_str_2 = _parse_param_str_2(d.pop("paramStr2"))

        def _parse_param_str_3(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        param_str_3 = _parse_param_str_3(d.pop("paramStr3"))

        def _parse_param_int_1(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        param_int_1 = _parse_param_int_1(d.pop("paramInt1"))

        def _parse_param_int_2(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        param_int_2 = _parse_param_int_2(d.pop("paramInt2"))

        def _parse_param_int_3(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        param_int_3 = _parse_param_int_3(d.pop("paramInt3"))

        file_info_id = d.pop("fileInfoId")

        def _parse_task_result(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        task_result = _parse_task_result(d.pop("taskResult"))

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

        job_task = cls(
            id=id,
            job_id=job_id,
            requested_execution_date=requested_execution_date,
            first_execution_date=first_execution_date,
            executed_date=executed_date,
            process_time_ms=process_time_ms,
            status=status,
            retry_counter=retry_counter,
            monitoring_id=monitoring_id,
            name=name,
            param_str_1=param_str_1,
            param_str_2=param_str_2,
            param_str_3=param_str_3,
            param_int_1=param_int_1,
            param_int_2=param_int_2,
            param_int_3=param_int_3,
            file_info_id=file_info_id,
            task_result=task_result,
            audit=audit,
        )

        return job_task
