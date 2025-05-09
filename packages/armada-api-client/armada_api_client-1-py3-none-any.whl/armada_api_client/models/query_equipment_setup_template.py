import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.e_order import EOrder
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryEquipmentSetupTemplate")


@_attrs_define
class QueryEquipmentSetupTemplate:
    """
    Attributes:
        id (Union[None, Unset, list[str]]):
        start (Union[None, Unset, int]):
        end (Union[None, Unset, int]):
        order (Union[EOrder, None, Unset]):
        sort (Union[None, Unset, str]):
        q (Union[None, Unset, str]):
        gt_modified_date_time (Union[None, Unset, datetime.datetime]):
        lt_modified_date_time (Union[None, Unset, datetime.datetime]):
        gt_created_date_time (Union[None, Unset, datetime.datetime]):
        lt_created_date_time (Union[None, Unset, datetime.datetime]):
        fields (Union[None, Unset, list[str]]):
        template_id (Union[None, Unset, list[int]]):
    """

    id: Union[None, Unset, list[str]] = UNSET
    start: Union[None, Unset, int] = UNSET
    end: Union[None, Unset, int] = UNSET
    order: Union[EOrder, None, Unset] = UNSET
    sort: Union[None, Unset, str] = UNSET
    q: Union[None, Unset, str] = UNSET
    gt_modified_date_time: Union[None, Unset, datetime.datetime] = UNSET
    lt_modified_date_time: Union[None, Unset, datetime.datetime] = UNSET
    gt_created_date_time: Union[None, Unset, datetime.datetime] = UNSET
    lt_created_date_time: Union[None, Unset, datetime.datetime] = UNSET
    fields: Union[None, Unset, list[str]] = UNSET
    template_id: Union[None, Unset, list[int]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id: Union[None, Unset, list[str]]
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, list):
            id = self.id

        else:
            id = self.id

        start: Union[None, Unset, int]
        if isinstance(self.start, Unset):
            start = UNSET
        else:
            start = self.start

        end: Union[None, Unset, int]
        if isinstance(self.end, Unset):
            end = UNSET
        else:
            end = self.end

        order: Union[None, Unset, str]
        if isinstance(self.order, Unset):
            order = UNSET
        elif isinstance(self.order, EOrder):
            order = self.order.value
        else:
            order = self.order

        sort: Union[None, Unset, str]
        if isinstance(self.sort, Unset):
            sort = UNSET
        else:
            sort = self.sort

        q: Union[None, Unset, str]
        if isinstance(self.q, Unset):
            q = UNSET
        else:
            q = self.q

        gt_modified_date_time: Union[None, Unset, str]
        if isinstance(self.gt_modified_date_time, Unset):
            gt_modified_date_time = UNSET
        elif isinstance(self.gt_modified_date_time, datetime.datetime):
            gt_modified_date_time = self.gt_modified_date_time.isoformat()
        else:
            gt_modified_date_time = self.gt_modified_date_time

        lt_modified_date_time: Union[None, Unset, str]
        if isinstance(self.lt_modified_date_time, Unset):
            lt_modified_date_time = UNSET
        elif isinstance(self.lt_modified_date_time, datetime.datetime):
            lt_modified_date_time = self.lt_modified_date_time.isoformat()
        else:
            lt_modified_date_time = self.lt_modified_date_time

        gt_created_date_time: Union[None, Unset, str]
        if isinstance(self.gt_created_date_time, Unset):
            gt_created_date_time = UNSET
        elif isinstance(self.gt_created_date_time, datetime.datetime):
            gt_created_date_time = self.gt_created_date_time.isoformat()
        else:
            gt_created_date_time = self.gt_created_date_time

        lt_created_date_time: Union[None, Unset, str]
        if isinstance(self.lt_created_date_time, Unset):
            lt_created_date_time = UNSET
        elif isinstance(self.lt_created_date_time, datetime.datetime):
            lt_created_date_time = self.lt_created_date_time.isoformat()
        else:
            lt_created_date_time = self.lt_created_date_time

        fields: Union[None, Unset, list[str]]
        if isinstance(self.fields, Unset):
            fields = UNSET
        elif isinstance(self.fields, list):
            fields = self.fields

        else:
            fields = self.fields

        template_id: Union[None, Unset, list[int]]
        if isinstance(self.template_id, Unset):
            template_id = UNSET
        elif isinstance(self.template_id, list):
            template_id = self.template_id

        else:
            template_id = self.template_id

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if order is not UNSET:
            field_dict["order"] = order
        if sort is not UNSET:
            field_dict["sort"] = sort
        if q is not UNSET:
            field_dict["q"] = q
        if gt_modified_date_time is not UNSET:
            field_dict["gtModifiedDateTime"] = gt_modified_date_time
        if lt_modified_date_time is not UNSET:
            field_dict["ltModifiedDateTime"] = lt_modified_date_time
        if gt_created_date_time is not UNSET:
            field_dict["gtCreatedDateTime"] = gt_created_date_time
        if lt_created_date_time is not UNSET:
            field_dict["ltCreatedDateTime"] = lt_created_date_time
        if fields is not UNSET:
            field_dict["fields"] = fields
        if template_id is not UNSET:
            field_dict["templateId"] = template_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_id(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                id_type_0 = cast(list[str], data)

                return id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_start(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        start = _parse_start(d.pop("start", UNSET))

        def _parse_end(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        end = _parse_end(d.pop("end", UNSET))

        def _parse_order(data: object) -> Union[EOrder, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                order_type_1 = EOrder(data)

                return order_type_1
            except:  # noqa: E722
                pass
            return cast(Union[EOrder, None, Unset], data)

        order = _parse_order(d.pop("order", UNSET))

        def _parse_sort(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sort = _parse_sort(d.pop("sort", UNSET))

        def _parse_q(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        q = _parse_q(d.pop("q", UNSET))

        def _parse_gt_modified_date_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                gt_modified_date_time_type_0 = isoparse(data)

                return gt_modified_date_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        gt_modified_date_time = _parse_gt_modified_date_time(d.pop("gtModifiedDateTime", UNSET))

        def _parse_lt_modified_date_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                lt_modified_date_time_type_0 = isoparse(data)

                return lt_modified_date_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        lt_modified_date_time = _parse_lt_modified_date_time(d.pop("ltModifiedDateTime", UNSET))

        def _parse_gt_created_date_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                gt_created_date_time_type_0 = isoparse(data)

                return gt_created_date_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        gt_created_date_time = _parse_gt_created_date_time(d.pop("gtCreatedDateTime", UNSET))

        def _parse_lt_created_date_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                lt_created_date_time_type_0 = isoparse(data)

                return lt_created_date_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        lt_created_date_time = _parse_lt_created_date_time(d.pop("ltCreatedDateTime", UNSET))

        def _parse_fields(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                fields_type_0 = cast(list[str], data)

                return fields_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        fields = _parse_fields(d.pop("fields", UNSET))

        def _parse_template_id(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                template_id_type_0 = cast(list[int], data)

                return template_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        template_id = _parse_template_id(d.pop("templateId", UNSET))

        query_equipment_setup_template = cls(
            id=id,
            start=start,
            end=end,
            order=order,
            sort=sort,
            q=q,
            gt_modified_date_time=gt_modified_date_time,
            lt_modified_date_time=lt_modified_date_time,
            gt_created_date_time=gt_created_date_time,
            lt_created_date_time=lt_created_date_time,
            fields=fields,
            template_id=template_id,
        )

        return query_equipment_setup_template
