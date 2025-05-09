import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.e_order import EOrder
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.criteria_string import CriteriaString


T = TypeVar("T", bound="QueryDescriptionElement")


@_attrs_define
class QueryDescriptionElement:
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
        equ_id (Union[None, Unset, list[int]]):
        equ_id_with_children (Union[Unset, bool]):
        custom_tree_node_id (Union[None, Unset, list[int]]):
        equ_type (Union[None, Unset, str]):
        equ_status (Union[None, Unset, str]):
        equ_path (Union[None, Unset, str]):
        equ_path_rel (Union[None, Unset, str]):
        equ_severity_type (Union[None, Unset, str]):
        equ_severity_type_min (Union[None, Unset, str]):
        equ_severity_level (Union[None, Unset, int]):
        equ_refresh_date_time_gt (Union[None, Unset, datetime.datetime]):
        equ_refresh_date_time_lt (Union[None, Unset, datetime.datetime]):
        equ_has_schematic (Union[None, Unset, bool]):
        equ_in_maintenance (Union[None, Unset, bool]):
        equ_has_active_alarm_with_name (Union[None, Unset, str]):
        equ_has_active_alarm_acknowledged (Union[None, Unset, bool]):
        equ_loc_country (Union[None, Unset, str]):
        equ_loc_region (Union[None, Unset, str]):
        equ_loc_province (Union[None, Unset, str]):
        equ_loc_city (Union[None, Unset, str]):
        equ_loc_group_1 (Union[None, Unset, str]):
        equ_loc_group_2 (Union[None, Unset, str]):
        equ_loc_group_3 (Union[None, Unset, str]):
        equ_loc_group_4 (Union[None, Unset, str]):
        equ_loc_group_5 (Union[None, Unset, str]):
        equ_loc_name (Union[None, Unset, str]):
        equ_loc_info (Union[None, Unset, str]):
        equ_loc_type (Union[None, Unset, int]):
        equ_criterias (Union[None, Unset, list['CriteriaString']]):
        group (Union[None, Unset, str]):
        sub_group (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        value (Union[None, Unset, str]):
        unit (Union[None, Unset, str]):
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
    equ_id: Union[None, Unset, list[int]] = UNSET
    equ_id_with_children: Union[Unset, bool] = UNSET
    custom_tree_node_id: Union[None, Unset, list[int]] = UNSET
    equ_type: Union[None, Unset, str] = UNSET
    equ_status: Union[None, Unset, str] = UNSET
    equ_path: Union[None, Unset, str] = UNSET
    equ_path_rel: Union[None, Unset, str] = UNSET
    equ_severity_type: Union[None, Unset, str] = UNSET
    equ_severity_type_min: Union[None, Unset, str] = UNSET
    equ_severity_level: Union[None, Unset, int] = UNSET
    equ_refresh_date_time_gt: Union[None, Unset, datetime.datetime] = UNSET
    equ_refresh_date_time_lt: Union[None, Unset, datetime.datetime] = UNSET
    equ_has_schematic: Union[None, Unset, bool] = UNSET
    equ_in_maintenance: Union[None, Unset, bool] = UNSET
    equ_has_active_alarm_with_name: Union[None, Unset, str] = UNSET
    equ_has_active_alarm_acknowledged: Union[None, Unset, bool] = UNSET
    equ_loc_country: Union[None, Unset, str] = UNSET
    equ_loc_region: Union[None, Unset, str] = UNSET
    equ_loc_province: Union[None, Unset, str] = UNSET
    equ_loc_city: Union[None, Unset, str] = UNSET
    equ_loc_group_1: Union[None, Unset, str] = UNSET
    equ_loc_group_2: Union[None, Unset, str] = UNSET
    equ_loc_group_3: Union[None, Unset, str] = UNSET
    equ_loc_group_4: Union[None, Unset, str] = UNSET
    equ_loc_group_5: Union[None, Unset, str] = UNSET
    equ_loc_name: Union[None, Unset, str] = UNSET
    equ_loc_info: Union[None, Unset, str] = UNSET
    equ_loc_type: Union[None, Unset, int] = UNSET
    equ_criterias: Union[None, Unset, list["CriteriaString"]] = UNSET
    group: Union[None, Unset, str] = UNSET
    sub_group: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    value: Union[None, Unset, str] = UNSET
    unit: Union[None, Unset, str] = UNSET

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

        equ_id: Union[None, Unset, list[int]]
        if isinstance(self.equ_id, Unset):
            equ_id = UNSET
        elif isinstance(self.equ_id, list):
            equ_id = self.equ_id

        else:
            equ_id = self.equ_id

        equ_id_with_children = self.equ_id_with_children

        custom_tree_node_id: Union[None, Unset, list[int]]
        if isinstance(self.custom_tree_node_id, Unset):
            custom_tree_node_id = UNSET
        elif isinstance(self.custom_tree_node_id, list):
            custom_tree_node_id = self.custom_tree_node_id

        else:
            custom_tree_node_id = self.custom_tree_node_id

        equ_type: Union[None, Unset, str]
        if isinstance(self.equ_type, Unset):
            equ_type = UNSET
        else:
            equ_type = self.equ_type

        equ_status: Union[None, Unset, str]
        if isinstance(self.equ_status, Unset):
            equ_status = UNSET
        else:
            equ_status = self.equ_status

        equ_path: Union[None, Unset, str]
        if isinstance(self.equ_path, Unset):
            equ_path = UNSET
        else:
            equ_path = self.equ_path

        equ_path_rel: Union[None, Unset, str]
        if isinstance(self.equ_path_rel, Unset):
            equ_path_rel = UNSET
        else:
            equ_path_rel = self.equ_path_rel

        equ_severity_type: Union[None, Unset, str]
        if isinstance(self.equ_severity_type, Unset):
            equ_severity_type = UNSET
        else:
            equ_severity_type = self.equ_severity_type

        equ_severity_type_min: Union[None, Unset, str]
        if isinstance(self.equ_severity_type_min, Unset):
            equ_severity_type_min = UNSET
        else:
            equ_severity_type_min = self.equ_severity_type_min

        equ_severity_level: Union[None, Unset, int]
        if isinstance(self.equ_severity_level, Unset):
            equ_severity_level = UNSET
        else:
            equ_severity_level = self.equ_severity_level

        equ_refresh_date_time_gt: Union[None, Unset, str]
        if isinstance(self.equ_refresh_date_time_gt, Unset):
            equ_refresh_date_time_gt = UNSET
        elif isinstance(self.equ_refresh_date_time_gt, datetime.datetime):
            equ_refresh_date_time_gt = self.equ_refresh_date_time_gt.isoformat()
        else:
            equ_refresh_date_time_gt = self.equ_refresh_date_time_gt

        equ_refresh_date_time_lt: Union[None, Unset, str]
        if isinstance(self.equ_refresh_date_time_lt, Unset):
            equ_refresh_date_time_lt = UNSET
        elif isinstance(self.equ_refresh_date_time_lt, datetime.datetime):
            equ_refresh_date_time_lt = self.equ_refresh_date_time_lt.isoformat()
        else:
            equ_refresh_date_time_lt = self.equ_refresh_date_time_lt

        equ_has_schematic: Union[None, Unset, bool]
        if isinstance(self.equ_has_schematic, Unset):
            equ_has_schematic = UNSET
        else:
            equ_has_schematic = self.equ_has_schematic

        equ_in_maintenance: Union[None, Unset, bool]
        if isinstance(self.equ_in_maintenance, Unset):
            equ_in_maintenance = UNSET
        else:
            equ_in_maintenance = self.equ_in_maintenance

        equ_has_active_alarm_with_name: Union[None, Unset, str]
        if isinstance(self.equ_has_active_alarm_with_name, Unset):
            equ_has_active_alarm_with_name = UNSET
        else:
            equ_has_active_alarm_with_name = self.equ_has_active_alarm_with_name

        equ_has_active_alarm_acknowledged: Union[None, Unset, bool]
        if isinstance(self.equ_has_active_alarm_acknowledged, Unset):
            equ_has_active_alarm_acknowledged = UNSET
        else:
            equ_has_active_alarm_acknowledged = self.equ_has_active_alarm_acknowledged

        equ_loc_country: Union[None, Unset, str]
        if isinstance(self.equ_loc_country, Unset):
            equ_loc_country = UNSET
        else:
            equ_loc_country = self.equ_loc_country

        equ_loc_region: Union[None, Unset, str]
        if isinstance(self.equ_loc_region, Unset):
            equ_loc_region = UNSET
        else:
            equ_loc_region = self.equ_loc_region

        equ_loc_province: Union[None, Unset, str]
        if isinstance(self.equ_loc_province, Unset):
            equ_loc_province = UNSET
        else:
            equ_loc_province = self.equ_loc_province

        equ_loc_city: Union[None, Unset, str]
        if isinstance(self.equ_loc_city, Unset):
            equ_loc_city = UNSET
        else:
            equ_loc_city = self.equ_loc_city

        equ_loc_group_1: Union[None, Unset, str]
        if isinstance(self.equ_loc_group_1, Unset):
            equ_loc_group_1 = UNSET
        else:
            equ_loc_group_1 = self.equ_loc_group_1

        equ_loc_group_2: Union[None, Unset, str]
        if isinstance(self.equ_loc_group_2, Unset):
            equ_loc_group_2 = UNSET
        else:
            equ_loc_group_2 = self.equ_loc_group_2

        equ_loc_group_3: Union[None, Unset, str]
        if isinstance(self.equ_loc_group_3, Unset):
            equ_loc_group_3 = UNSET
        else:
            equ_loc_group_3 = self.equ_loc_group_3

        equ_loc_group_4: Union[None, Unset, str]
        if isinstance(self.equ_loc_group_4, Unset):
            equ_loc_group_4 = UNSET
        else:
            equ_loc_group_4 = self.equ_loc_group_4

        equ_loc_group_5: Union[None, Unset, str]
        if isinstance(self.equ_loc_group_5, Unset):
            equ_loc_group_5 = UNSET
        else:
            equ_loc_group_5 = self.equ_loc_group_5

        equ_loc_name: Union[None, Unset, str]
        if isinstance(self.equ_loc_name, Unset):
            equ_loc_name = UNSET
        else:
            equ_loc_name = self.equ_loc_name

        equ_loc_info: Union[None, Unset, str]
        if isinstance(self.equ_loc_info, Unset):
            equ_loc_info = UNSET
        else:
            equ_loc_info = self.equ_loc_info

        equ_loc_type: Union[None, Unset, int]
        if isinstance(self.equ_loc_type, Unset):
            equ_loc_type = UNSET
        else:
            equ_loc_type = self.equ_loc_type

        equ_criterias: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.equ_criterias, Unset):
            equ_criterias = UNSET
        elif isinstance(self.equ_criterias, list):
            equ_criterias = []
            for equ_criterias_type_0_item_data in self.equ_criterias:
                equ_criterias_type_0_item = equ_criterias_type_0_item_data.to_dict()
                equ_criterias.append(equ_criterias_type_0_item)

        else:
            equ_criterias = self.equ_criterias

        group: Union[None, Unset, str]
        if isinstance(self.group, Unset):
            group = UNSET
        else:
            group = self.group

        sub_group: Union[None, Unset, str]
        if isinstance(self.sub_group, Unset):
            sub_group = UNSET
        else:
            sub_group = self.sub_group

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        value: Union[None, Unset, str]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        unit: Union[None, Unset, str]
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

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
        if equ_id is not UNSET:
            field_dict["equId"] = equ_id
        if equ_id_with_children is not UNSET:
            field_dict["equIdWithChildren"] = equ_id_with_children
        if custom_tree_node_id is not UNSET:
            field_dict["customTreeNodeId"] = custom_tree_node_id
        if equ_type is not UNSET:
            field_dict["equType"] = equ_type
        if equ_status is not UNSET:
            field_dict["equStatus"] = equ_status
        if equ_path is not UNSET:
            field_dict["equPath"] = equ_path
        if equ_path_rel is not UNSET:
            field_dict["equPathRel"] = equ_path_rel
        if equ_severity_type is not UNSET:
            field_dict["equSeverityType"] = equ_severity_type
        if equ_severity_type_min is not UNSET:
            field_dict["equSeverityTypeMin"] = equ_severity_type_min
        if equ_severity_level is not UNSET:
            field_dict["equSeverityLevel"] = equ_severity_level
        if equ_refresh_date_time_gt is not UNSET:
            field_dict["equRefreshDateTimeGt"] = equ_refresh_date_time_gt
        if equ_refresh_date_time_lt is not UNSET:
            field_dict["equRefreshDateTimeLt"] = equ_refresh_date_time_lt
        if equ_has_schematic is not UNSET:
            field_dict["equHasSchematic"] = equ_has_schematic
        if equ_in_maintenance is not UNSET:
            field_dict["equInMaintenance"] = equ_in_maintenance
        if equ_has_active_alarm_with_name is not UNSET:
            field_dict["equHasActiveAlarmWithName"] = equ_has_active_alarm_with_name
        if equ_has_active_alarm_acknowledged is not UNSET:
            field_dict["equHasActiveAlarmAcknowledged"] = equ_has_active_alarm_acknowledged
        if equ_loc_country is not UNSET:
            field_dict["equLocCountry"] = equ_loc_country
        if equ_loc_region is not UNSET:
            field_dict["equLocRegion"] = equ_loc_region
        if equ_loc_province is not UNSET:
            field_dict["equLocProvince"] = equ_loc_province
        if equ_loc_city is not UNSET:
            field_dict["equLocCity"] = equ_loc_city
        if equ_loc_group_1 is not UNSET:
            field_dict["equLocGroup1"] = equ_loc_group_1
        if equ_loc_group_2 is not UNSET:
            field_dict["equLocGroup2"] = equ_loc_group_2
        if equ_loc_group_3 is not UNSET:
            field_dict["equLocGroup3"] = equ_loc_group_3
        if equ_loc_group_4 is not UNSET:
            field_dict["equLocGroup4"] = equ_loc_group_4
        if equ_loc_group_5 is not UNSET:
            field_dict["equLocGroup5"] = equ_loc_group_5
        if equ_loc_name is not UNSET:
            field_dict["equLocName"] = equ_loc_name
        if equ_loc_info is not UNSET:
            field_dict["equLocInfo"] = equ_loc_info
        if equ_loc_type is not UNSET:
            field_dict["equLocType"] = equ_loc_type
        if equ_criterias is not UNSET:
            field_dict["equCriterias"] = equ_criterias
        if group is not UNSET:
            field_dict["group"] = group
        if sub_group is not UNSET:
            field_dict["subGroup"] = sub_group
        if name is not UNSET:
            field_dict["name"] = name
        if value is not UNSET:
            field_dict["value"] = value
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.criteria_string import CriteriaString

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

        def _parse_equ_id(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                equ_id_type_0 = cast(list[int], data)

                return equ_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        equ_id = _parse_equ_id(d.pop("equId", UNSET))

        equ_id_with_children = d.pop("equIdWithChildren", UNSET)

        def _parse_custom_tree_node_id(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                custom_tree_node_id_type_0 = cast(list[int], data)

                return custom_tree_node_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        custom_tree_node_id = _parse_custom_tree_node_id(d.pop("customTreeNodeId", UNSET))

        def _parse_equ_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_type = _parse_equ_type(d.pop("equType", UNSET))

        def _parse_equ_status(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_status = _parse_equ_status(d.pop("equStatus", UNSET))

        def _parse_equ_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_path = _parse_equ_path(d.pop("equPath", UNSET))

        def _parse_equ_path_rel(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_path_rel = _parse_equ_path_rel(d.pop("equPathRel", UNSET))

        def _parse_equ_severity_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_severity_type = _parse_equ_severity_type(d.pop("equSeverityType", UNSET))

        def _parse_equ_severity_type_min(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_severity_type_min = _parse_equ_severity_type_min(d.pop("equSeverityTypeMin", UNSET))

        def _parse_equ_severity_level(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        equ_severity_level = _parse_equ_severity_level(d.pop("equSeverityLevel", UNSET))

        def _parse_equ_refresh_date_time_gt(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                equ_refresh_date_time_gt_type_0 = isoparse(data)

                return equ_refresh_date_time_gt_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        equ_refresh_date_time_gt = _parse_equ_refresh_date_time_gt(d.pop("equRefreshDateTimeGt", UNSET))

        def _parse_equ_refresh_date_time_lt(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                equ_refresh_date_time_lt_type_0 = isoparse(data)

                return equ_refresh_date_time_lt_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        equ_refresh_date_time_lt = _parse_equ_refresh_date_time_lt(d.pop("equRefreshDateTimeLt", UNSET))

        def _parse_equ_has_schematic(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        equ_has_schematic = _parse_equ_has_schematic(d.pop("equHasSchematic", UNSET))

        def _parse_equ_in_maintenance(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        equ_in_maintenance = _parse_equ_in_maintenance(d.pop("equInMaintenance", UNSET))

        def _parse_equ_has_active_alarm_with_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_has_active_alarm_with_name = _parse_equ_has_active_alarm_with_name(
            d.pop("equHasActiveAlarmWithName", UNSET)
        )

        def _parse_equ_has_active_alarm_acknowledged(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        equ_has_active_alarm_acknowledged = _parse_equ_has_active_alarm_acknowledged(
            d.pop("equHasActiveAlarmAcknowledged", UNSET)
        )

        def _parse_equ_loc_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_country = _parse_equ_loc_country(d.pop("equLocCountry", UNSET))

        def _parse_equ_loc_region(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_region = _parse_equ_loc_region(d.pop("equLocRegion", UNSET))

        def _parse_equ_loc_province(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_province = _parse_equ_loc_province(d.pop("equLocProvince", UNSET))

        def _parse_equ_loc_city(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_city = _parse_equ_loc_city(d.pop("equLocCity", UNSET))

        def _parse_equ_loc_group_1(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_group_1 = _parse_equ_loc_group_1(d.pop("equLocGroup1", UNSET))

        def _parse_equ_loc_group_2(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_group_2 = _parse_equ_loc_group_2(d.pop("equLocGroup2", UNSET))

        def _parse_equ_loc_group_3(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_group_3 = _parse_equ_loc_group_3(d.pop("equLocGroup3", UNSET))

        def _parse_equ_loc_group_4(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_group_4 = _parse_equ_loc_group_4(d.pop("equLocGroup4", UNSET))

        def _parse_equ_loc_group_5(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_group_5 = _parse_equ_loc_group_5(d.pop("equLocGroup5", UNSET))

        def _parse_equ_loc_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_name = _parse_equ_loc_name(d.pop("equLocName", UNSET))

        def _parse_equ_loc_info(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        equ_loc_info = _parse_equ_loc_info(d.pop("equLocInfo", UNSET))

        def _parse_equ_loc_type(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        equ_loc_type = _parse_equ_loc_type(d.pop("equLocType", UNSET))

        def _parse_equ_criterias(data: object) -> Union[None, Unset, list["CriteriaString"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                equ_criterias_type_0 = []
                _equ_criterias_type_0 = data
                for equ_criterias_type_0_item_data in _equ_criterias_type_0:
                    equ_criterias_type_0_item = CriteriaString.from_dict(equ_criterias_type_0_item_data)

                    equ_criterias_type_0.append(equ_criterias_type_0_item)

                return equ_criterias_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CriteriaString"]], data)

        equ_criterias = _parse_equ_criterias(d.pop("equCriterias", UNSET))

        def _parse_group(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group = _parse_group(d.pop("group", UNSET))

        def _parse_sub_group(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sub_group = _parse_sub_group(d.pop("subGroup", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        value = _parse_value(d.pop("value", UNSET))

        def _parse_unit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        unit = _parse_unit(d.pop("unit", UNSET))

        query_description_element = cls(
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
            equ_id=equ_id,
            equ_id_with_children=equ_id_with_children,
            custom_tree_node_id=custom_tree_node_id,
            equ_type=equ_type,
            equ_status=equ_status,
            equ_path=equ_path,
            equ_path_rel=equ_path_rel,
            equ_severity_type=equ_severity_type,
            equ_severity_type_min=equ_severity_type_min,
            equ_severity_level=equ_severity_level,
            equ_refresh_date_time_gt=equ_refresh_date_time_gt,
            equ_refresh_date_time_lt=equ_refresh_date_time_lt,
            equ_has_schematic=equ_has_schematic,
            equ_in_maintenance=equ_in_maintenance,
            equ_has_active_alarm_with_name=equ_has_active_alarm_with_name,
            equ_has_active_alarm_acknowledged=equ_has_active_alarm_acknowledged,
            equ_loc_country=equ_loc_country,
            equ_loc_region=equ_loc_region,
            equ_loc_province=equ_loc_province,
            equ_loc_city=equ_loc_city,
            equ_loc_group_1=equ_loc_group_1,
            equ_loc_group_2=equ_loc_group_2,
            equ_loc_group_3=equ_loc_group_3,
            equ_loc_group_4=equ_loc_group_4,
            equ_loc_group_5=equ_loc_group_5,
            equ_loc_name=equ_loc_name,
            equ_loc_info=equ_loc_info,
            equ_loc_type=equ_loc_type,
            equ_criterias=equ_criterias,
            group=group,
            sub_group=sub_group,
            name=name,
            value=value,
            unit=unit,
        )

        return query_description_element
