from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MonitoringSyncOptions")


@_attrs_define
class MonitoringSyncOptions:
    """
    Attributes:
        description (Union[Unset, bool]):
        alarm (Union[Unset, bool]):
        event (Union[Unset, bool]):
        data (Union[Unset, bool]):
        data_record (Union[Unset, bool]):
        control (Union[Unset, bool]):
        config (Union[Unset, bool]):
        data_record_day (Union[Unset, bool]):
        data_record_hour (Union[Unset, bool]):
        data_record_minute (Union[Unset, bool]):
        data_record_delta (Union[Unset, bool]):
        equ_path (Union[None, Unset, str]):
        data_record_next (Union[Unset, int]):
        data_record_id (Union[Unset, int]):
        use_data_record_last_minute (Union[Unset, bool]):
        use_data_record_last_hour (Union[Unset, bool]):
        use_data_record_last_day (Union[Unset, bool]):
        use_data_record_last_delta (Union[Unset, bool]):
    """

    description: Union[Unset, bool] = UNSET
    alarm: Union[Unset, bool] = UNSET
    event: Union[Unset, bool] = UNSET
    data: Union[Unset, bool] = UNSET
    data_record: Union[Unset, bool] = UNSET
    control: Union[Unset, bool] = UNSET
    config: Union[Unset, bool] = UNSET
    data_record_day: Union[Unset, bool] = UNSET
    data_record_hour: Union[Unset, bool] = UNSET
    data_record_minute: Union[Unset, bool] = UNSET
    data_record_delta: Union[Unset, bool] = UNSET
    equ_path: Union[None, Unset, str] = UNSET
    data_record_next: Union[Unset, int] = UNSET
    data_record_id: Union[Unset, int] = UNSET
    use_data_record_last_minute: Union[Unset, bool] = UNSET
    use_data_record_last_hour: Union[Unset, bool] = UNSET
    use_data_record_last_day: Union[Unset, bool] = UNSET
    use_data_record_last_delta: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        alarm = self.alarm

        event = self.event

        data = self.data

        data_record = self.data_record

        control = self.control

        config = self.config

        data_record_day = self.data_record_day

        data_record_hour = self.data_record_hour

        data_record_minute = self.data_record_minute

        data_record_delta = self.data_record_delta

        equ_path: Union[None, Unset, str]
        if isinstance(self.equ_path, Unset):
            equ_path = UNSET
        else:
            equ_path = self.equ_path

        data_record_next = self.data_record_next

        data_record_id = self.data_record_id

        use_data_record_last_minute = self.use_data_record_last_minute

        use_data_record_last_hour = self.use_data_record_last_hour

        use_data_record_last_day = self.use_data_record_last_day

        use_data_record_last_delta = self.use_data_record_last_delta

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if alarm is not UNSET:
            field_dict["alarm"] = alarm
        if event is not UNSET:
            field_dict["event"] = event
        if data is not UNSET:
            field_dict["data"] = data
        if data_record is not UNSET:
            field_dict["dataRecord"] = data_record
        if control is not UNSET:
            field_dict["control"] = control
        if config is not UNSET:
            field_dict["config"] = config
        if data_record_day is not UNSET:
            field_dict["dataRecordDay"] = data_record_day
        if data_record_hour is not UNSET:
            field_dict["dataRecordHour"] = data_record_hour
        if data_record_minute is not UNSET:
            field_dict["dataRecordMinute"] = data_record_minute
        if data_record_delta is not UNSET:
            field_dict["dataRecordDelta"] = data_record_delta
        if equ_path is not UNSET:
            field_dict["equPath"] = equ_path
        if data_record_next is not UNSET:
            field_dict["dataRecordNext"] = data_record_next
        if data_record_id is not UNSET:
            field_dict["dataRecordId"] = data_record_id
        if use_data_record_last_minute is not UNSET:
            field_dict["useDataRecordLastMinute"] = use_data_record_last_minute
        if use_data_record_last_hour is not UNSET:
            field_dict["useDataRecordLastHour"] = use_data_record_last_hour
        if use_data_record_last_day is not UNSET:
            field_dict["useDataRecordLastDay"] = use_data_record_last_day
        if use_data_record_last_delta is not UNSET:
            field_dict["useDataRecordLastDelta"] = use_data_record_last_delta

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        alarm = d.pop("alarm", UNSET)

        event = d.pop("event", UNSET)

        data = d.pop("data", UNSET)

        data_record = d.pop("dataRecord", UNSET)

        control = d.pop("control", UNSET)

        config = d.pop("config", UNSET)

        data_record_day = d.pop("dataRecordDay", UNSET)

        data_record_hour = d.pop("dataRecordHour", UNSET)

        data_record_minute = d.pop("dataRecordMinute", UNSET)

        data_record_delta = d.pop("dataRecordDelta", UNSET)

        def _parse_equ_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_path = _parse_equ_path(d.pop("equPath", UNSET))

        data_record_next = d.pop("dataRecordNext", UNSET)

        data_record_id = d.pop("dataRecordId", UNSET)

        use_data_record_last_minute = d.pop("useDataRecordLastMinute", UNSET)

        use_data_record_last_hour = d.pop("useDataRecordLastHour", UNSET)

        use_data_record_last_day = d.pop("useDataRecordLastDay", UNSET)

        use_data_record_last_delta = d.pop("useDataRecordLastDelta", UNSET)

        monitoring_sync_options = cls(
            description=description,
            alarm=alarm,
            event=event,
            data=data,
            data_record=data_record,
            control=control,
            config=config,
            data_record_day=data_record_day,
            data_record_hour=data_record_hour,
            data_record_minute=data_record_minute,
            data_record_delta=data_record_delta,
            equ_path=equ_path,
            data_record_next=data_record_next,
            data_record_id=data_record_id,
            use_data_record_last_minute=use_data_record_last_minute,
            use_data_record_last_hour=use_data_record_last_hour,
            use_data_record_last_day=use_data_record_last_day,
            use_data_record_last_delta=use_data_record_last_delta,
        )

        return monitoring_sync_options
