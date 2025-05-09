from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_specifications_type_0 import AssetSpecificationsType0
    from ..models.metric import Metric


T = TypeVar("T", bound="Asset")


@_attrs_define
class Asset:
    """
    Attributes:
        global_site_id (Union[Unset, int]):
        id (Union[Unset, int]):
        type_ (Union[None, Unset, str]):
        specifications (Union['AssetSpecificationsType0', None, Unset]):
        metrics (Union[None, Unset, list['Metric']]):
    """

    global_site_id: Union[Unset, int] = UNSET
    id: Union[Unset, int] = UNSET
    type_: Union[None, Unset, str] = UNSET
    specifications: Union["AssetSpecificationsType0", None, Unset] = UNSET
    metrics: Union[None, Unset, list["Metric"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.asset_specifications_type_0 import AssetSpecificationsType0

        global_site_id = self.global_site_id

        id = self.id

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        specifications: Union[None, Unset, dict[str, Any]]
        if isinstance(self.specifications, Unset):
            specifications = UNSET
        elif isinstance(self.specifications, AssetSpecificationsType0):
            specifications = self.specifications.to_dict()
        else:
            specifications = self.specifications

        metrics: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.metrics, Unset):
            metrics = UNSET
        elif isinstance(self.metrics, list):
            metrics = []
            for metrics_type_0_item_data in self.metrics:
                metrics_type_0_item = metrics_type_0_item_data.to_dict()
                metrics.append(metrics_type_0_item)

        else:
            metrics = self.metrics

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if global_site_id is not UNSET:
            field_dict["globalSiteId"] = global_site_id
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if specifications is not UNSET:
            field_dict["specifications"] = specifications
        if metrics is not UNSET:
            field_dict["metrics"] = metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_specifications_type_0 import AssetSpecificationsType0
        from ..models.metric import Metric

        d = dict(src_dict)
        global_site_id = d.pop("globalSiteId", UNSET)

        id = d.pop("id", UNSET)

        def _parse_type_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_specifications(data: object) -> Union["AssetSpecificationsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                specifications_type_0 = AssetSpecificationsType0.from_dict(data)

                return specifications_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AssetSpecificationsType0", None, Unset], data)

        specifications = _parse_specifications(d.pop("specifications", UNSET))

        def _parse_metrics(data: object) -> Union[None, Unset, list["Metric"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                metrics_type_0 = []
                _metrics_type_0 = data
                for metrics_type_0_item_data in _metrics_type_0:
                    metrics_type_0_item = Metric.from_dict(metrics_type_0_item_data)

                    metrics_type_0.append(metrics_type_0_item)

                return metrics_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Metric"]], data)

        metrics = _parse_metrics(d.pop("metrics", UNSET))

        asset = cls(
            global_site_id=global_site_id,
            id=id,
            type_=type_,
            specifications=specifications,
            metrics=metrics,
        )

        return asset
