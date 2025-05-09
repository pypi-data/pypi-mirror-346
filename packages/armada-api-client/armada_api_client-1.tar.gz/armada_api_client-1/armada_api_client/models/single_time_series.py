from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.date_value import DateValue
    from ..models.single_time_series_header_type_0 import SingleTimeSeriesHeaderType0


T = TypeVar("T", bound="SingleTimeSeries")


@_attrs_define
class SingleTimeSeries:
    """
    Attributes:
        header (Union['SingleTimeSeriesHeaderType0', None]):
        values (Union[None, list['DateValue']]):
    """

    header: Union["SingleTimeSeriesHeaderType0", None]
    values: Union[None, list["DateValue"]]

    def to_dict(self) -> dict[str, Any]:
        from ..models.single_time_series_header_type_0 import SingleTimeSeriesHeaderType0

        header: Union[None, dict[str, Any]]
        if isinstance(self.header, SingleTimeSeriesHeaderType0):
            header = self.header.to_dict()
        else:
            header = self.header

        values: Union[None, list[dict[str, Any]]]
        if isinstance(self.values, list):
            values = []
            for values_type_0_item_data in self.values:
                values_type_0_item = values_type_0_item_data.to_dict()
                values.append(values_type_0_item)

        else:
            values = self.values

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "header": header,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.date_value import DateValue
        from ..models.single_time_series_header_type_0 import SingleTimeSeriesHeaderType0

        d = dict(src_dict)

        def _parse_header(data: object) -> Union["SingleTimeSeriesHeaderType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                header_type_0 = SingleTimeSeriesHeaderType0.from_dict(data)

                return header_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SingleTimeSeriesHeaderType0", None], data)

        header = _parse_header(d.pop("header"))

        def _parse_values(data: object) -> Union[None, list["DateValue"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                values_type_0 = []
                _values_type_0 = data
                for values_type_0_item_data in _values_type_0:
                    values_type_0_item = DateValue.from_dict(values_type_0_item_data)

                    values_type_0.append(values_type_0_item)

                return values_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["DateValue"]], data)

        values = _parse_values(d.pop("values"))

        single_time_series = cls(
            header=header,
            values=values,
        )

        return single_time_series
