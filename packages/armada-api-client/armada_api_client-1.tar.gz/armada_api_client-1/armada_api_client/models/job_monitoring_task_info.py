from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobMonitoringTaskInfo")


@_attrs_define
class JobMonitoringTaskInfo:
    """
    Attributes:
        monitoring_id (int):
        task_name (str):
        comment (Union[None, Unset, str]):
        param_str_1 (Union[None, Unset, str]):
        param_str_2 (Union[None, Unset, str]):
        param_str_3 (Union[None, Unset, str]):
        param_int_1 (Union[None, Unset, str]):
        param_int_2 (Union[None, Unset, str]):
        param_int_3 (Union[None, Unset, str]):
        file_info_id (Union[Unset, int]):
    """

    monitoring_id: int
    task_name: str
    comment: Union[None, Unset, str] = UNSET
    param_str_1: Union[None, Unset, str] = UNSET
    param_str_2: Union[None, Unset, str] = UNSET
    param_str_3: Union[None, Unset, str] = UNSET
    param_int_1: Union[None, Unset, str] = UNSET
    param_int_2: Union[None, Unset, str] = UNSET
    param_int_3: Union[None, Unset, str] = UNSET
    file_info_id: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        monitoring_id = self.monitoring_id

        task_name = self.task_name

        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        param_str_1: Union[None, Unset, str]
        if isinstance(self.param_str_1, Unset):
            param_str_1 = UNSET
        else:
            param_str_1 = self.param_str_1

        param_str_2: Union[None, Unset, str]
        if isinstance(self.param_str_2, Unset):
            param_str_2 = UNSET
        else:
            param_str_2 = self.param_str_2

        param_str_3: Union[None, Unset, str]
        if isinstance(self.param_str_3, Unset):
            param_str_3 = UNSET
        else:
            param_str_3 = self.param_str_3

        param_int_1: Union[None, Unset, str]
        if isinstance(self.param_int_1, Unset):
            param_int_1 = UNSET
        else:
            param_int_1 = self.param_int_1

        param_int_2: Union[None, Unset, str]
        if isinstance(self.param_int_2, Unset):
            param_int_2 = UNSET
        else:
            param_int_2 = self.param_int_2

        param_int_3: Union[None, Unset, str]
        if isinstance(self.param_int_3, Unset):
            param_int_3 = UNSET
        else:
            param_int_3 = self.param_int_3

        file_info_id = self.file_info_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "monitoringId": monitoring_id,
                "taskName": task_name,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment
        if param_str_1 is not UNSET:
            field_dict["paramStr1"] = param_str_1
        if param_str_2 is not UNSET:
            field_dict["paramStr2"] = param_str_2
        if param_str_3 is not UNSET:
            field_dict["paramStr3"] = param_str_3
        if param_int_1 is not UNSET:
            field_dict["paramInt1"] = param_int_1
        if param_int_2 is not UNSET:
            field_dict["paramInt2"] = param_int_2
        if param_int_3 is not UNSET:
            field_dict["paramInt3"] = param_int_3
        if file_info_id is not UNSET:
            field_dict["fileInfoId"] = file_info_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        monitoring_id = d.pop("monitoringId")

        task_name = d.pop("taskName")

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        def _parse_param_str_1(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        param_str_1 = _parse_param_str_1(d.pop("paramStr1", UNSET))

        def _parse_param_str_2(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        param_str_2 = _parse_param_str_2(d.pop("paramStr2", UNSET))

        def _parse_param_str_3(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        param_str_3 = _parse_param_str_3(d.pop("paramStr3", UNSET))

        def _parse_param_int_1(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        param_int_1 = _parse_param_int_1(d.pop("paramInt1", UNSET))

        def _parse_param_int_2(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        param_int_2 = _parse_param_int_2(d.pop("paramInt2", UNSET))

        def _parse_param_int_3(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        param_int_3 = _parse_param_int_3(d.pop("paramInt3", UNSET))

        file_info_id = d.pop("fileInfoId", UNSET)

        job_monitoring_task_info = cls(
            monitoring_id=monitoring_id,
            task_name=task_name,
            comment=comment,
            param_str_1=param_str_1,
            param_str_2=param_str_2,
            param_str_3=param_str_3,
            param_int_1=param_int_1,
            param_int_2=param_int_2,
            param_int_3=param_int_3,
            file_info_id=file_info_id,
        )

        return job_monitoring_task_info
