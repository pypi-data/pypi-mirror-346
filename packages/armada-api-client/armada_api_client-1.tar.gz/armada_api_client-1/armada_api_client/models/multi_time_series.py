from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.date_values import DateValues
    from ..models.multi_time_series_headers_type_0_item import MultiTimeSeriesHeadersType0Item


T = TypeVar("T", bound="MultiTimeSeries")


@_attrs_define
class MultiTimeSeries:
    """
    Attributes:
        headers (Union[None, Unset, list['MultiTimeSeriesHeadersType0Item']]):
        values (Union[None, Unset, list['DateValues']]):
    """

    headers: Union[None, Unset, list["MultiTimeSeriesHeadersType0Item"]] = UNSET
    values: Union[None, Unset, list["DateValues"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        headers: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.headers, Unset):
            headers = UNSET
        elif isinstance(self.headers, list):
            headers = []
            for headers_type_0_item_data in self.headers:
                headers_type_0_item = headers_type_0_item_data.to_dict()
                headers.append(headers_type_0_item)

        else:
            headers = self.headers

        values: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.values, Unset):
            values = UNSET
        elif isinstance(self.values, list):
            values = []
            for values_type_0_item_data in self.values:
                values_type_0_item = values_type_0_item_data.to_dict()
                values.append(values_type_0_item)

        else:
            values = self.values

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if headers is not UNSET:
            field_dict["headers"] = headers
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.date_values import DateValues
        from ..models.multi_time_series_headers_type_0_item import MultiTimeSeriesHeadersType0Item

        d = dict(src_dict)

        def _parse_headers(data: object) -> Union[None, Unset, list["MultiTimeSeriesHeadersType0Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                headers_type_0 = []
                _headers_type_0 = data
                for headers_type_0_item_data in _headers_type_0:
                    headers_type_0_item = MultiTimeSeriesHeadersType0Item.from_dict(headers_type_0_item_data)

                    headers_type_0.append(headers_type_0_item)

                return headers_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["MultiTimeSeriesHeadersType0Item"]], data)

        headers = _parse_headers(d.pop("headers", UNSET))

        def _parse_values(data: object) -> Union[None, Unset, list["DateValues"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                values_type_0 = []
                _values_type_0 = data
                for values_type_0_item_data in _values_type_0:
                    values_type_0_item = DateValues.from_dict(values_type_0_item_data)

                    values_type_0.append(values_type_0_item)

                return values_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["DateValues"]], data)

        values = _parse_values(d.pop("values", UNSET))

        multi_time_series = cls(
            headers=headers,
            values=values,
        )

        return multi_time_series
