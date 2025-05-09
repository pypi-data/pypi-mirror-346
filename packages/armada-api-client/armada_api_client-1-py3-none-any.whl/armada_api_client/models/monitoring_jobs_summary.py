import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="MonitoringJobsSummary")


@_attrs_define
class MonitoringJobsSummary:
    """
    Attributes:
        monitoring_id (int):
        last_job (Union[None, datetime.datetime]):
        get_count (int):
        get_start (Union[None, datetime.datetime]):
        get_state (Union[None, str]):
        get_progress_info (Union[None, str]):
        post_count (int):
        post_start (Union[None, datetime.datetime]):
        post_state (Union[None, str]):
        post_progress_info (Union[None, str]):
        event_count (int):
        event_start (Union[None, datetime.datetime]):
        event_state (Union[None, str]):
        event_progress_info (Union[None, str]):
        task_count (int):
        task_name (Union[None, str]):
        task_start (Union[None, datetime.datetime]):
        task_state (Union[None, str]):
        task_progress_info (Union[None, str]):
        id (Union[None, Unset, str]):
    """

    monitoring_id: int
    last_job: Union[None, datetime.datetime]
    get_count: int
    get_start: Union[None, datetime.datetime]
    get_state: Union[None, str]
    get_progress_info: Union[None, str]
    post_count: int
    post_start: Union[None, datetime.datetime]
    post_state: Union[None, str]
    post_progress_info: Union[None, str]
    event_count: int
    event_start: Union[None, datetime.datetime]
    event_state: Union[None, str]
    event_progress_info: Union[None, str]
    task_count: int
    task_name: Union[None, str]
    task_start: Union[None, datetime.datetime]
    task_state: Union[None, str]
    task_progress_info: Union[None, str]
    id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        monitoring_id = self.monitoring_id

        last_job: Union[None, str]
        if isinstance(self.last_job, datetime.datetime):
            last_job = self.last_job.isoformat()
        else:
            last_job = self.last_job

        get_count = self.get_count

        get_start: Union[None, str]
        if isinstance(self.get_start, datetime.datetime):
            get_start = self.get_start.isoformat()
        else:
            get_start = self.get_start

        get_state: Union[None, str]
        get_state = self.get_state

        get_progress_info: Union[None, str]
        get_progress_info = self.get_progress_info

        post_count = self.post_count

        post_start: Union[None, str]
        if isinstance(self.post_start, datetime.datetime):
            post_start = self.post_start.isoformat()
        else:
            post_start = self.post_start

        post_state: Union[None, str]
        post_state = self.post_state

        post_progress_info: Union[None, str]
        post_progress_info = self.post_progress_info

        event_count = self.event_count

        event_start: Union[None, str]
        if isinstance(self.event_start, datetime.datetime):
            event_start = self.event_start.isoformat()
        else:
            event_start = self.event_start

        event_state: Union[None, str]
        event_state = self.event_state

        event_progress_info: Union[None, str]
        event_progress_info = self.event_progress_info

        task_count = self.task_count

        task_name: Union[None, str]
        task_name = self.task_name

        task_start: Union[None, str]
        if isinstance(self.task_start, datetime.datetime):
            task_start = self.task_start.isoformat()
        else:
            task_start = self.task_start

        task_state: Union[None, str]
        task_state = self.task_state

        task_progress_info: Union[None, str]
        task_progress_info = self.task_progress_info

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "monitoringId": monitoring_id,
                "lastJob": last_job,
                "getCount": get_count,
                "getStart": get_start,
                "getState": get_state,
                "getProgressInfo": get_progress_info,
                "postCount": post_count,
                "postStart": post_start,
                "postState": post_state,
                "postProgressInfo": post_progress_info,
                "eventCount": event_count,
                "eventStart": event_start,
                "eventState": event_state,
                "eventProgressInfo": event_progress_info,
                "taskCount": task_count,
                "taskName": task_name,
                "taskStart": task_start,
                "taskState": task_state,
                "taskProgressInfo": task_progress_info,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        monitoring_id = d.pop("monitoringId")

        def _parse_last_job(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_job_type_0 = isoparse(data)

                return last_job_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_job = _parse_last_job(d.pop("lastJob"))

        get_count = d.pop("getCount")

        def _parse_get_start(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                get_start_type_0 = isoparse(data)

                return get_start_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        get_start = _parse_get_start(d.pop("getStart"))

        def _parse_get_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        get_state = _parse_get_state(d.pop("getState"))

        def _parse_get_progress_info(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        get_progress_info = _parse_get_progress_info(d.pop("getProgressInfo"))

        post_count = d.pop("postCount")

        def _parse_post_start(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                post_start_type_0 = isoparse(data)

                return post_start_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        post_start = _parse_post_start(d.pop("postStart"))

        def _parse_post_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        post_state = _parse_post_state(d.pop("postState"))

        def _parse_post_progress_info(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        post_progress_info = _parse_post_progress_info(d.pop("postProgressInfo"))

        event_count = d.pop("eventCount")

        def _parse_event_start(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                event_start_type_0 = isoparse(data)

                return event_start_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        event_start = _parse_event_start(d.pop("eventStart"))

        def _parse_event_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        event_state = _parse_event_state(d.pop("eventState"))

        def _parse_event_progress_info(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        event_progress_info = _parse_event_progress_info(d.pop("eventProgressInfo"))

        task_count = d.pop("taskCount")

        def _parse_task_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        task_name = _parse_task_name(d.pop("taskName"))

        def _parse_task_start(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_start_type_0 = isoparse(data)

                return task_start_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        task_start = _parse_task_start(d.pop("taskStart"))

        def _parse_task_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        task_state = _parse_task_state(d.pop("taskState"))

        def _parse_task_progress_info(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        task_progress_info = _parse_task_progress_info(d.pop("taskProgressInfo"))

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        monitoring_jobs_summary = cls(
            monitoring_id=monitoring_id,
            last_job=last_job,
            get_count=get_count,
            get_start=get_start,
            get_state=get_state,
            get_progress_info=get_progress_info,
            post_count=post_count,
            post_start=post_start,
            post_state=post_state,
            post_progress_info=post_progress_info,
            event_count=event_count,
            event_start=event_start,
            event_state=event_state,
            event_progress_info=event_progress_info,
            task_count=task_count,
            task_name=task_name,
            task_start=task_start,
            task_state=task_state,
            task_progress_info=task_progress_info,
            id=id,
        )

        return monitoring_jobs_summary
