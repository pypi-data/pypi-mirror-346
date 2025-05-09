from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.monitoring_sync_options import MonitoringSyncOptions
    from ..models.query_monitoring import QueryMonitoring


T = TypeVar("T", bound="QueryRefreshMonitorings")


@_attrs_define
class QueryRefreshMonitorings:
    """
    Attributes:
        sync_options (MonitoringSyncOptions):
        monitoring_selection (QueryMonitoring):
    """

    sync_options: "MonitoringSyncOptions"
    monitoring_selection: "QueryMonitoring"

    def to_dict(self) -> dict[str, Any]:
        sync_options = self.sync_options.to_dict()

        monitoring_selection = self.monitoring_selection.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "syncOptions": sync_options,
                "monitoringSelection": monitoring_selection,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.monitoring_sync_options import MonitoringSyncOptions
        from ..models.query_monitoring import QueryMonitoring

        d = dict(src_dict)
        sync_options = MonitoringSyncOptions.from_dict(d.pop("syncOptions"))

        monitoring_selection = QueryMonitoring.from_dict(d.pop("monitoringSelection"))

        query_refresh_monitorings = cls(
            sync_options=sync_options,
            monitoring_selection=monitoring_selection,
        )

        return query_refresh_monitorings
