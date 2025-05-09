from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.monitorings_stats import MonitoringsStats
    from ..models.users_stats import UsersStats


T = TypeVar("T", bound="TenantStats")


@_attrs_define
class TenantStats:
    """
    Attributes:
        id (Union[None, str]):
        ready (bool):
        monitorings (Union['MonitoringsStats', None]):
        users (Union['UsersStats', None]):
    """

    id: Union[None, str]
    ready: bool
    monitorings: Union["MonitoringsStats", None]
    users: Union["UsersStats", None]

    def to_dict(self) -> dict[str, Any]:
        from ..models.monitorings_stats import MonitoringsStats
        from ..models.users_stats import UsersStats

        id: Union[None, str]
        id = self.id

        ready = self.ready

        monitorings: Union[None, dict[str, Any]]
        if isinstance(self.monitorings, MonitoringsStats):
            monitorings = self.monitorings.to_dict()
        else:
            monitorings = self.monitorings

        users: Union[None, dict[str, Any]]
        if isinstance(self.users, UsersStats):
            users = self.users.to_dict()
        else:
            users = self.users

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "ready": ready,
                "monitorings": monitorings,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.monitorings_stats import MonitoringsStats
        from ..models.users_stats import UsersStats

        d = dict(src_dict)

        def _parse_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        id = _parse_id(d.pop("id"))

        ready = d.pop("ready")

        def _parse_monitorings(data: object) -> Union["MonitoringsStats", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                monitorings_type_1 = MonitoringsStats.from_dict(data)

                return monitorings_type_1
            except:  # noqa: E722
                pass
            return cast(Union["MonitoringsStats", None], data)

        monitorings = _parse_monitorings(d.pop("monitorings"))

        def _parse_users(data: object) -> Union["UsersStats", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                users_type_1 = UsersStats.from_dict(data)

                return users_type_1
            except:  # noqa: E722
                pass
            return cast(Union["UsersStats", None], data)

        users = _parse_users(d.pop("users"))

        tenant_stats = cls(
            id=id,
            ready=ready,
            monitorings=monitorings,
            users=users,
        )

        return tenant_stats
