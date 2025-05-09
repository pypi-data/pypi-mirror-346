from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.user_stat import UserStat


T = TypeVar("T", bound="UsersStats")


@_attrs_define
class UsersStats:
    """
    Attributes:
        count (int):
        last_5_active (Union[None, list['UserStat']]):
    """

    count: int
    last_5_active: Union[None, list["UserStat"]]

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        last_5_active: Union[None, list[dict[str, Any]]]
        if isinstance(self.last_5_active, list):
            last_5_active = []
            for last_5_active_type_0_item_data in self.last_5_active:
                last_5_active_type_0_item = last_5_active_type_0_item_data.to_dict()
                last_5_active.append(last_5_active_type_0_item)

        else:
            last_5_active = self.last_5_active

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "count": count,
                "last5Active": last_5_active,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_stat import UserStat

        d = dict(src_dict)
        count = d.pop("count")

        def _parse_last_5_active(data: object) -> Union[None, list["UserStat"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                last_5_active_type_0 = []
                _last_5_active_type_0 = data
                for last_5_active_type_0_item_data in _last_5_active_type_0:
                    last_5_active_type_0_item = UserStat.from_dict(last_5_active_type_0_item_data)

                    last_5_active_type_0.append(last_5_active_type_0_item)

                return last_5_active_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["UserStat"]], data)

        last_5_active = _parse_last_5_active(d.pop("last5Active"))

        users_stats = cls(
            count=count,
            last_5_active=last_5_active,
        )

        return users_stats
