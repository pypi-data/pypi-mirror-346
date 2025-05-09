from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.job_monitoring_task_info import JobMonitoringTaskInfo


T = TypeVar("T", bound="JobMonitoringTaskInfoRequest")


@_attrs_define
class JobMonitoringTaskInfoRequest:
    """
    Attributes:
        job_monitoring_task_info (JobMonitoringTaskInfo):
        monitoring_ids (Union[None, list[int]]):
    """

    job_monitoring_task_info: "JobMonitoringTaskInfo"
    monitoring_ids: Union[None, list[int]]

    def to_dict(self) -> dict[str, Any]:
        job_monitoring_task_info = self.job_monitoring_task_info.to_dict()

        monitoring_ids: Union[None, list[int]]
        if isinstance(self.monitoring_ids, list):
            monitoring_ids = self.monitoring_ids

        else:
            monitoring_ids = self.monitoring_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "jobMonitoringTaskInfo": job_monitoring_task_info,
                "monitoringIds": monitoring_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_monitoring_task_info import JobMonitoringTaskInfo

        d = dict(src_dict)
        job_monitoring_task_info = JobMonitoringTaskInfo.from_dict(d.pop("jobMonitoringTaskInfo"))

        def _parse_monitoring_ids(data: object) -> Union[None, list[int]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                monitoring_ids_type_0 = cast(list[int], data)

                return monitoring_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[int]], data)

        monitoring_ids = _parse_monitoring_ids(d.pop("monitoringIds"))

        job_monitoring_task_info_request = cls(
            job_monitoring_task_info=job_monitoring_task_info,
            monitoring_ids=monitoring_ids,
        )

        return job_monitoring_task_info_request
