import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.e_order import EOrder
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryMonitoring")


@_attrs_define
class QueryMonitoring:
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
        loc_country (Union[None, Unset, str]):
        loc_region (Union[None, Unset, str]):
        loc_province (Union[None, Unset, str]):
        loc_city (Union[None, Unset, str]):
        loc_group_1 (Union[None, Unset, str]):
        loc_group_2 (Union[None, Unset, str]):
        loc_group_3 (Union[None, Unset, str]):
        loc_group_4 (Union[None, Unset, str]):
        loc_group_5 (Union[None, Unset, str]):
        loc_name (Union[None, Unset, str]):
        loc_info (Union[None, Unset, str]):
        loc_type (Union[None, Unset, int]):
        q_loc (Union[None, Unset, str]):
        mon_connection_status (Union[None, Unset, str]):
        mon_type (Union[None, Unset, str]):
        mon_ip_address (Union[None, Unset, str]):
        monitoring_id (Union[None, Unset, list[int]]):
        mon_status (Union[None, Unset, str]):
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
    loc_country: Union[None, Unset, str] = UNSET
    loc_region: Union[None, Unset, str] = UNSET
    loc_province: Union[None, Unset, str] = UNSET
    loc_city: Union[None, Unset, str] = UNSET
    loc_group_1: Union[None, Unset, str] = UNSET
    loc_group_2: Union[None, Unset, str] = UNSET
    loc_group_3: Union[None, Unset, str] = UNSET
    loc_group_4: Union[None, Unset, str] = UNSET
    loc_group_5: Union[None, Unset, str] = UNSET
    loc_name: Union[None, Unset, str] = UNSET
    loc_info: Union[None, Unset, str] = UNSET
    loc_type: Union[None, Unset, int] = UNSET
    q_loc: Union[None, Unset, str] = UNSET
    mon_connection_status: Union[None, Unset, str] = UNSET
    mon_type: Union[None, Unset, str] = UNSET
    mon_ip_address: Union[None, Unset, str] = UNSET
    monitoring_id: Union[None, Unset, list[int]] = UNSET
    mon_status: Union[None, Unset, str] = UNSET

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

        loc_country: Union[None, Unset, str]
        if isinstance(self.loc_country, Unset):
            loc_country = UNSET
        else:
            loc_country = self.loc_country

        loc_region: Union[None, Unset, str]
        if isinstance(self.loc_region, Unset):
            loc_region = UNSET
        else:
            loc_region = self.loc_region

        loc_province: Union[None, Unset, str]
        if isinstance(self.loc_province, Unset):
            loc_province = UNSET
        else:
            loc_province = self.loc_province

        loc_city: Union[None, Unset, str]
        if isinstance(self.loc_city, Unset):
            loc_city = UNSET
        else:
            loc_city = self.loc_city

        loc_group_1: Union[None, Unset, str]
        if isinstance(self.loc_group_1, Unset):
            loc_group_1 = UNSET
        else:
            loc_group_1 = self.loc_group_1

        loc_group_2: Union[None, Unset, str]
        if isinstance(self.loc_group_2, Unset):
            loc_group_2 = UNSET
        else:
            loc_group_2 = self.loc_group_2

        loc_group_3: Union[None, Unset, str]
        if isinstance(self.loc_group_3, Unset):
            loc_group_3 = UNSET
        else:
            loc_group_3 = self.loc_group_3

        loc_group_4: Union[None, Unset, str]
        if isinstance(self.loc_group_4, Unset):
            loc_group_4 = UNSET
        else:
            loc_group_4 = self.loc_group_4

        loc_group_5: Union[None, Unset, str]
        if isinstance(self.loc_group_5, Unset):
            loc_group_5 = UNSET
        else:
            loc_group_5 = self.loc_group_5

        loc_name: Union[None, Unset, str]
        if isinstance(self.loc_name, Unset):
            loc_name = UNSET
        else:
            loc_name = self.loc_name

        loc_info: Union[None, Unset, str]
        if isinstance(self.loc_info, Unset):
            loc_info = UNSET
        else:
            loc_info = self.loc_info

        loc_type: Union[None, Unset, int]
        if isinstance(self.loc_type, Unset):
            loc_type = UNSET
        else:
            loc_type = self.loc_type

        q_loc: Union[None, Unset, str]
        if isinstance(self.q_loc, Unset):
            q_loc = UNSET
        else:
            q_loc = self.q_loc

        mon_connection_status: Union[None, Unset, str]
        if isinstance(self.mon_connection_status, Unset):
            mon_connection_status = UNSET
        else:
            mon_connection_status = self.mon_connection_status

        mon_type: Union[None, Unset, str]
        if isinstance(self.mon_type, Unset):
            mon_type = UNSET
        else:
            mon_type = self.mon_type

        mon_ip_address: Union[None, Unset, str]
        if isinstance(self.mon_ip_address, Unset):
            mon_ip_address = UNSET
        else:
            mon_ip_address = self.mon_ip_address

        monitoring_id: Union[None, Unset, list[int]]
        if isinstance(self.monitoring_id, Unset):
            monitoring_id = UNSET
        elif isinstance(self.monitoring_id, list):
            monitoring_id = self.monitoring_id

        else:
            monitoring_id = self.monitoring_id

        mon_status: Union[None, Unset, str]
        if isinstance(self.mon_status, Unset):
            mon_status = UNSET
        else:
            mon_status = self.mon_status

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
        if loc_country is not UNSET:
            field_dict["locCountry"] = loc_country
        if loc_region is not UNSET:
            field_dict["locRegion"] = loc_region
        if loc_province is not UNSET:
            field_dict["locProvince"] = loc_province
        if loc_city is not UNSET:
            field_dict["locCity"] = loc_city
        if loc_group_1 is not UNSET:
            field_dict["locGroup1"] = loc_group_1
        if loc_group_2 is not UNSET:
            field_dict["locGroup2"] = loc_group_2
        if loc_group_3 is not UNSET:
            field_dict["locGroup3"] = loc_group_3
        if loc_group_4 is not UNSET:
            field_dict["locGroup4"] = loc_group_4
        if loc_group_5 is not UNSET:
            field_dict["locGroup5"] = loc_group_5
        if loc_name is not UNSET:
            field_dict["locName"] = loc_name
        if loc_info is not UNSET:
            field_dict["locInfo"] = loc_info
        if loc_type is not UNSET:
            field_dict["locType"] = loc_type
        if q_loc is not UNSET:
            field_dict["qLoc"] = q_loc
        if mon_connection_status is not UNSET:
            field_dict["monConnectionStatus"] = mon_connection_status
        if mon_type is not UNSET:
            field_dict["monType"] = mon_type
        if mon_ip_address is not UNSET:
            field_dict["monIpAddress"] = mon_ip_address
        if monitoring_id is not UNSET:
            field_dict["monitoringId"] = monitoring_id
        if mon_status is not UNSET:
            field_dict["monStatus"] = mon_status

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

        def _parse_loc_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_country = _parse_loc_country(d.pop("locCountry", UNSET))

        def _parse_loc_region(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_region = _parse_loc_region(d.pop("locRegion", UNSET))

        def _parse_loc_province(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_province = _parse_loc_province(d.pop("locProvince", UNSET))

        def _parse_loc_city(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_city = _parse_loc_city(d.pop("locCity", UNSET))

        def _parse_loc_group_1(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_group_1 = _parse_loc_group_1(d.pop("locGroup1", UNSET))

        def _parse_loc_group_2(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_group_2 = _parse_loc_group_2(d.pop("locGroup2", UNSET))

        def _parse_loc_group_3(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_group_3 = _parse_loc_group_3(d.pop("locGroup3", UNSET))

        def _parse_loc_group_4(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_group_4 = _parse_loc_group_4(d.pop("locGroup4", UNSET))

        def _parse_loc_group_5(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_group_5 = _parse_loc_group_5(d.pop("locGroup5", UNSET))

        def _parse_loc_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_name = _parse_loc_name(d.pop("locName", UNSET))

        def _parse_loc_info(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        loc_info = _parse_loc_info(d.pop("locInfo", UNSET))

        def _parse_loc_type(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        loc_type = _parse_loc_type(d.pop("locType", UNSET))

        def _parse_q_loc(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        q_loc = _parse_q_loc(d.pop("qLoc", UNSET))

        def _parse_mon_connection_status(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mon_connection_status = _parse_mon_connection_status(d.pop("monConnectionStatus", UNSET))

        def _parse_mon_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mon_type = _parse_mon_type(d.pop("monType", UNSET))

        def _parse_mon_ip_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mon_ip_address = _parse_mon_ip_address(d.pop("monIpAddress", UNSET))

        def _parse_monitoring_id(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                monitoring_id_type_0 = cast(list[int], data)

                return monitoring_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        monitoring_id = _parse_monitoring_id(d.pop("monitoringId", UNSET))

        def _parse_mon_status(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mon_status = _parse_mon_status(d.pop("monStatus", UNSET))

        query_monitoring = cls(
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
            loc_country=loc_country,
            loc_region=loc_region,
            loc_province=loc_province,
            loc_city=loc_city,
            loc_group_1=loc_group_1,
            loc_group_2=loc_group_2,
            loc_group_3=loc_group_3,
            loc_group_4=loc_group_4,
            loc_group_5=loc_group_5,
            loc_name=loc_name,
            loc_info=loc_info,
            loc_type=loc_type,
            q_loc=q_loc,
            mon_connection_status=mon_connection_status,
            mon_type=mon_type,
            mon_ip_address=mon_ip_address,
            monitoring_id=monitoring_id,
            mon_status=mon_status,
        )

        return query_monitoring
