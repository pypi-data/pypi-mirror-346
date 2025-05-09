import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="MqttConnection")


@_attrs_define
class MqttConnection:
    """
    Attributes:
        id (str):
        device_id (Union[None, str]):
        client_id (Union[None, str]):
        monitoring_id (int):
        machine_name (Union[None, Unset, str]):
        broker_id (Union[None, Unset, str]):
        last_login (Union[None, Unset, datetime.datetime]):
        last_disconnect (Union[None, Unset, datetime.datetime]):
        last_activity (Union[None, Unset, datetime.datetime]):
        connected (Union[Unset, bool]):
        sent_count (Union[Unset, int]):
        received_count (Union[Unset, int]):
        sent_kb (Union[Unset, float]):
        received_kb (Union[Unset, float]):
        heartbeat_count (Union[Unset, int]):
        last_heart_beat (Union[Unset, datetime.datetime]):
        endpoint (Union[None, Unset, str]):
        subscribed_request_topic (Union[Unset, bool]):
    """

    id: str
    device_id: Union[None, str]
    client_id: Union[None, str]
    monitoring_id: int
    machine_name: Union[None, Unset, str] = UNSET
    broker_id: Union[None, Unset, str] = UNSET
    last_login: Union[None, Unset, datetime.datetime] = UNSET
    last_disconnect: Union[None, Unset, datetime.datetime] = UNSET
    last_activity: Union[None, Unset, datetime.datetime] = UNSET
    connected: Union[Unset, bool] = UNSET
    sent_count: Union[Unset, int] = UNSET
    received_count: Union[Unset, int] = UNSET
    sent_kb: Union[Unset, float] = UNSET
    received_kb: Union[Unset, float] = UNSET
    heartbeat_count: Union[Unset, int] = UNSET
    last_heart_beat: Union[Unset, datetime.datetime] = UNSET
    endpoint: Union[None, Unset, str] = UNSET
    subscribed_request_topic: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        device_id: Union[None, str]
        device_id = self.device_id

        client_id: Union[None, str]
        client_id = self.client_id

        monitoring_id = self.monitoring_id

        machine_name: Union[None, Unset, str]
        if isinstance(self.machine_name, Unset):
            machine_name = UNSET
        else:
            machine_name = self.machine_name

        broker_id: Union[None, Unset, str]
        if isinstance(self.broker_id, Unset):
            broker_id = UNSET
        else:
            broker_id = self.broker_id

        last_login: Union[None, Unset, str]
        if isinstance(self.last_login, Unset):
            last_login = UNSET
        elif isinstance(self.last_login, datetime.datetime):
            last_login = self.last_login.isoformat()
        else:
            last_login = self.last_login

        last_disconnect: Union[None, Unset, str]
        if isinstance(self.last_disconnect, Unset):
            last_disconnect = UNSET
        elif isinstance(self.last_disconnect, datetime.datetime):
            last_disconnect = self.last_disconnect.isoformat()
        else:
            last_disconnect = self.last_disconnect

        last_activity: Union[None, Unset, str]
        if isinstance(self.last_activity, Unset):
            last_activity = UNSET
        elif isinstance(self.last_activity, datetime.datetime):
            last_activity = self.last_activity.isoformat()
        else:
            last_activity = self.last_activity

        connected = self.connected

        sent_count = self.sent_count

        received_count = self.received_count

        sent_kb = self.sent_kb

        received_kb = self.received_kb

        heartbeat_count = self.heartbeat_count

        last_heart_beat: Union[Unset, str] = UNSET
        if not isinstance(self.last_heart_beat, Unset):
            last_heart_beat = self.last_heart_beat.isoformat()

        endpoint: Union[None, Unset, str]
        if isinstance(self.endpoint, Unset):
            endpoint = UNSET
        else:
            endpoint = self.endpoint

        subscribed_request_topic = self.subscribed_request_topic

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "deviceId": device_id,
                "clientId": client_id,
                "monitoringId": monitoring_id,
            }
        )
        if machine_name is not UNSET:
            field_dict["machineName"] = machine_name
        if broker_id is not UNSET:
            field_dict["brokerId"] = broker_id
        if last_login is not UNSET:
            field_dict["lastLogin"] = last_login
        if last_disconnect is not UNSET:
            field_dict["lastDisconnect"] = last_disconnect
        if last_activity is not UNSET:
            field_dict["lastActivity"] = last_activity
        if connected is not UNSET:
            field_dict["connected"] = connected
        if sent_count is not UNSET:
            field_dict["sentCount"] = sent_count
        if received_count is not UNSET:
            field_dict["receivedCount"] = received_count
        if sent_kb is not UNSET:
            field_dict["sentKb"] = sent_kb
        if received_kb is not UNSET:
            field_dict["receivedKb"] = received_kb
        if heartbeat_count is not UNSET:
            field_dict["heartbeatCount"] = heartbeat_count
        if last_heart_beat is not UNSET:
            field_dict["lastHeartBeat"] = last_heart_beat
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if subscribed_request_topic is not UNSET:
            field_dict["subscribedRequestTopic"] = subscribed_request_topic

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_device_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        device_id = _parse_device_id(d.pop("deviceId"))

        def _parse_client_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        client_id = _parse_client_id(d.pop("clientId"))

        monitoring_id = d.pop("monitoringId")

        def _parse_machine_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        machine_name = _parse_machine_name(d.pop("machineName", UNSET))

        def _parse_broker_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        broker_id = _parse_broker_id(d.pop("brokerId", UNSET))

        def _parse_last_login(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_login_type_0 = isoparse(data)

                return last_login_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_login = _parse_last_login(d.pop("lastLogin", UNSET))

        def _parse_last_disconnect(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_disconnect_type_0 = isoparse(data)

                return last_disconnect_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_disconnect = _parse_last_disconnect(d.pop("lastDisconnect", UNSET))

        def _parse_last_activity(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_activity_type_0 = isoparse(data)

                return last_activity_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_activity = _parse_last_activity(d.pop("lastActivity", UNSET))

        connected = d.pop("connected", UNSET)

        sent_count = d.pop("sentCount", UNSET)

        received_count = d.pop("receivedCount", UNSET)

        sent_kb = d.pop("sentKb", UNSET)

        received_kb = d.pop("receivedKb", UNSET)

        heartbeat_count = d.pop("heartbeatCount", UNSET)

        _last_heart_beat = d.pop("lastHeartBeat", UNSET)
        last_heart_beat: Union[Unset, datetime.datetime]
        if isinstance(_last_heart_beat, Unset):
            last_heart_beat = UNSET
        else:
            last_heart_beat = isoparse(_last_heart_beat)

        def _parse_endpoint(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        endpoint = _parse_endpoint(d.pop("endpoint", UNSET))

        subscribed_request_topic = d.pop("subscribedRequestTopic", UNSET)

        mqtt_connection = cls(
            id=id,
            device_id=device_id,
            client_id=client_id,
            monitoring_id=monitoring_id,
            machine_name=machine_name,
            broker_id=broker_id,
            last_login=last_login,
            last_disconnect=last_disconnect,
            last_activity=last_activity,
            connected=connected,
            sent_count=sent_count,
            received_count=received_count,
            sent_kb=sent_kb,
            received_kb=received_kb,
            heartbeat_count=heartbeat_count,
            last_heart_beat=last_heart_beat,
            endpoint=endpoint,
            subscribed_request_topic=subscribed_request_topic,
        )

        return mqtt_connection
