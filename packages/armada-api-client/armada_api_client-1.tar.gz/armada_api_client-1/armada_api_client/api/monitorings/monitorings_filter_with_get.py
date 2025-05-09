import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.e_order import EOrder
from ...models.monitoring import Monitoring
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    mon_connection_status: Union[Unset, str] = UNSET,
    mon_type: Union[Unset, str] = UNSET,
    mon_ip_address: Union[Unset, str] = UNSET,
    monitoring_id: Union[Unset, list[int]] = UNSET,
    mon_status: Union[Unset, str] = UNSET,
    loc_country: Union[Unset, str] = UNSET,
    loc_region: Union[Unset, str] = UNSET,
    loc_province: Union[Unset, str] = UNSET,
    loc_city: Union[Unset, str] = UNSET,
    loc_group_1: Union[Unset, str] = UNSET,
    loc_group_2: Union[Unset, str] = UNSET,
    loc_group_3: Union[Unset, str] = UNSET,
    loc_group_4: Union[Unset, str] = UNSET,
    loc_group_5: Union[Unset, str] = UNSET,
    loc_name: Union[Unset, str] = UNSET,
    loc_info: Union[Unset, str] = UNSET,
    loc_type: Union[Unset, int] = UNSET,
    q_loc: Union[Unset, str] = UNSET,
    id: Union[Unset, list[str]] = UNSET,
    field_start: Union[Unset, int] = UNSET,
    field_end: Union[Unset, int] = UNSET,
    field_order: Union[Unset, EOrder] = UNSET,
    field_sort: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    gt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    gt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    fields: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["monConnectionStatus"] = mon_connection_status

    params["monType"] = mon_type

    params["monIpAddress"] = mon_ip_address

    json_monitoring_id: Union[Unset, list[int]] = UNSET
    if not isinstance(monitoring_id, Unset):
        json_monitoring_id = monitoring_id

    params["monitoringId"] = json_monitoring_id

    params["monStatus"] = mon_status

    params["locCountry"] = loc_country

    params["locRegion"] = loc_region

    params["locProvince"] = loc_province

    params["locCity"] = loc_city

    params["locGroup1"] = loc_group_1

    params["locGroup2"] = loc_group_2

    params["locGroup3"] = loc_group_3

    params["locGroup4"] = loc_group_4

    params["locGroup5"] = loc_group_5

    params["locName"] = loc_name

    params["locInfo"] = loc_info

    params["locType"] = loc_type

    params["qLoc"] = q_loc

    json_id: Union[Unset, list[str]] = UNSET
    if not isinstance(id, Unset):
        json_id = id

    params["id"] = json_id

    params["_start"] = field_start

    params["_end"] = field_end

    json_field_order: Union[Unset, str] = UNSET
    if not isinstance(field_order, Unset):
        json_field_order = field_order.value

    params["_order"] = json_field_order

    params["_sort"] = field_sort

    params["q"] = q

    json_gt_modified_date_time: Union[Unset, str] = UNSET
    if not isinstance(gt_modified_date_time, Unset):
        json_gt_modified_date_time = gt_modified_date_time.isoformat()
    params["gtModifiedDateTime"] = json_gt_modified_date_time

    json_lt_modified_date_time: Union[Unset, str] = UNSET
    if not isinstance(lt_modified_date_time, Unset):
        json_lt_modified_date_time = lt_modified_date_time.isoformat()
    params["ltModifiedDateTime"] = json_lt_modified_date_time

    json_gt_created_date_time: Union[Unset, str] = UNSET
    if not isinstance(gt_created_date_time, Unset):
        json_gt_created_date_time = gt_created_date_time.isoformat()
    params["gtCreatedDateTime"] = json_gt_created_date_time

    json_lt_created_date_time: Union[Unset, str] = UNSET
    if not isinstance(lt_created_date_time, Unset):
        json_lt_created_date_time = lt_created_date_time.isoformat()
    params["ltCreatedDateTime"] = json_lt_created_date_time

    json_fields: Union[Unset, list[str]] = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Monitorings",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ProblemDetails, list["Monitoring"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Monitoring.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = ProblemDetails.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = ProblemDetails.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ProblemDetails, list["Monitoring"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    mon_connection_status: Union[Unset, str] = UNSET,
    mon_type: Union[Unset, str] = UNSET,
    mon_ip_address: Union[Unset, str] = UNSET,
    monitoring_id: Union[Unset, list[int]] = UNSET,
    mon_status: Union[Unset, str] = UNSET,
    loc_country: Union[Unset, str] = UNSET,
    loc_region: Union[Unset, str] = UNSET,
    loc_province: Union[Unset, str] = UNSET,
    loc_city: Union[Unset, str] = UNSET,
    loc_group_1: Union[Unset, str] = UNSET,
    loc_group_2: Union[Unset, str] = UNSET,
    loc_group_3: Union[Unset, str] = UNSET,
    loc_group_4: Union[Unset, str] = UNSET,
    loc_group_5: Union[Unset, str] = UNSET,
    loc_name: Union[Unset, str] = UNSET,
    loc_info: Union[Unset, str] = UNSET,
    loc_type: Union[Unset, int] = UNSET,
    q_loc: Union[Unset, str] = UNSET,
    id: Union[Unset, list[str]] = UNSET,
    field_start: Union[Unset, int] = UNSET,
    field_end: Union[Unset, int] = UNSET,
    field_order: Union[Unset, EOrder] = UNSET,
    field_sort: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    gt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    gt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    fields: Union[Unset, list[str]] = UNSET,
) -> Response[Union[ProblemDetails, list["Monitoring"]]]:
    """Get list of object matching filter (Auth policies: ElementRead)

     Get list of object matching filter. Optionnal fields can be requested in the response by using
    fields query parameters

    Args:
        mon_connection_status (Union[Unset, str]):
        mon_type (Union[Unset, str]):
        mon_ip_address (Union[Unset, str]):
        monitoring_id (Union[Unset, list[int]]):
        mon_status (Union[Unset, str]):
        loc_country (Union[Unset, str]):
        loc_region (Union[Unset, str]):
        loc_province (Union[Unset, str]):
        loc_city (Union[Unset, str]):
        loc_group_1 (Union[Unset, str]):
        loc_group_2 (Union[Unset, str]):
        loc_group_3 (Union[Unset, str]):
        loc_group_4 (Union[Unset, str]):
        loc_group_5 (Union[Unset, str]):
        loc_name (Union[Unset, str]):
        loc_info (Union[Unset, str]):
        loc_type (Union[Unset, int]):
        q_loc (Union[Unset, str]):
        id (Union[Unset, list[str]]):
        field_start (Union[Unset, int]):
        field_end (Union[Unset, int]):
        field_order (Union[Unset, EOrder]):
        field_sort (Union[Unset, str]):
        q (Union[Unset, str]):
        gt_modified_date_time (Union[Unset, datetime.datetime]):
        lt_modified_date_time (Union[Unset, datetime.datetime]):
        gt_created_date_time (Union[Unset, datetime.datetime]):
        lt_created_date_time (Union[Unset, datetime.datetime]):
        fields (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, list['Monitoring']]]
    """

    kwargs = _get_kwargs(
        mon_connection_status=mon_connection_status,
        mon_type=mon_type,
        mon_ip_address=mon_ip_address,
        monitoring_id=monitoring_id,
        mon_status=mon_status,
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
        id=id,
        field_start=field_start,
        field_end=field_end,
        field_order=field_order,
        field_sort=field_sort,
        q=q,
        gt_modified_date_time=gt_modified_date_time,
        lt_modified_date_time=lt_modified_date_time,
        gt_created_date_time=gt_created_date_time,
        lt_created_date_time=lt_created_date_time,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    mon_connection_status: Union[Unset, str] = UNSET,
    mon_type: Union[Unset, str] = UNSET,
    mon_ip_address: Union[Unset, str] = UNSET,
    monitoring_id: Union[Unset, list[int]] = UNSET,
    mon_status: Union[Unset, str] = UNSET,
    loc_country: Union[Unset, str] = UNSET,
    loc_region: Union[Unset, str] = UNSET,
    loc_province: Union[Unset, str] = UNSET,
    loc_city: Union[Unset, str] = UNSET,
    loc_group_1: Union[Unset, str] = UNSET,
    loc_group_2: Union[Unset, str] = UNSET,
    loc_group_3: Union[Unset, str] = UNSET,
    loc_group_4: Union[Unset, str] = UNSET,
    loc_group_5: Union[Unset, str] = UNSET,
    loc_name: Union[Unset, str] = UNSET,
    loc_info: Union[Unset, str] = UNSET,
    loc_type: Union[Unset, int] = UNSET,
    q_loc: Union[Unset, str] = UNSET,
    id: Union[Unset, list[str]] = UNSET,
    field_start: Union[Unset, int] = UNSET,
    field_end: Union[Unset, int] = UNSET,
    field_order: Union[Unset, EOrder] = UNSET,
    field_sort: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    gt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    gt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    fields: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[ProblemDetails, list["Monitoring"]]]:
    """Get list of object matching filter (Auth policies: ElementRead)

     Get list of object matching filter. Optionnal fields can be requested in the response by using
    fields query parameters

    Args:
        mon_connection_status (Union[Unset, str]):
        mon_type (Union[Unset, str]):
        mon_ip_address (Union[Unset, str]):
        monitoring_id (Union[Unset, list[int]]):
        mon_status (Union[Unset, str]):
        loc_country (Union[Unset, str]):
        loc_region (Union[Unset, str]):
        loc_province (Union[Unset, str]):
        loc_city (Union[Unset, str]):
        loc_group_1 (Union[Unset, str]):
        loc_group_2 (Union[Unset, str]):
        loc_group_3 (Union[Unset, str]):
        loc_group_4 (Union[Unset, str]):
        loc_group_5 (Union[Unset, str]):
        loc_name (Union[Unset, str]):
        loc_info (Union[Unset, str]):
        loc_type (Union[Unset, int]):
        q_loc (Union[Unset, str]):
        id (Union[Unset, list[str]]):
        field_start (Union[Unset, int]):
        field_end (Union[Unset, int]):
        field_order (Union[Unset, EOrder]):
        field_sort (Union[Unset, str]):
        q (Union[Unset, str]):
        gt_modified_date_time (Union[Unset, datetime.datetime]):
        lt_modified_date_time (Union[Unset, datetime.datetime]):
        gt_created_date_time (Union[Unset, datetime.datetime]):
        lt_created_date_time (Union[Unset, datetime.datetime]):
        fields (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, list['Monitoring']]
    """

    return sync_detailed(
        client=client,
        mon_connection_status=mon_connection_status,
        mon_type=mon_type,
        mon_ip_address=mon_ip_address,
        monitoring_id=monitoring_id,
        mon_status=mon_status,
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
        id=id,
        field_start=field_start,
        field_end=field_end,
        field_order=field_order,
        field_sort=field_sort,
        q=q,
        gt_modified_date_time=gt_modified_date_time,
        lt_modified_date_time=lt_modified_date_time,
        gt_created_date_time=gt_created_date_time,
        lt_created_date_time=lt_created_date_time,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    mon_connection_status: Union[Unset, str] = UNSET,
    mon_type: Union[Unset, str] = UNSET,
    mon_ip_address: Union[Unset, str] = UNSET,
    monitoring_id: Union[Unset, list[int]] = UNSET,
    mon_status: Union[Unset, str] = UNSET,
    loc_country: Union[Unset, str] = UNSET,
    loc_region: Union[Unset, str] = UNSET,
    loc_province: Union[Unset, str] = UNSET,
    loc_city: Union[Unset, str] = UNSET,
    loc_group_1: Union[Unset, str] = UNSET,
    loc_group_2: Union[Unset, str] = UNSET,
    loc_group_3: Union[Unset, str] = UNSET,
    loc_group_4: Union[Unset, str] = UNSET,
    loc_group_5: Union[Unset, str] = UNSET,
    loc_name: Union[Unset, str] = UNSET,
    loc_info: Union[Unset, str] = UNSET,
    loc_type: Union[Unset, int] = UNSET,
    q_loc: Union[Unset, str] = UNSET,
    id: Union[Unset, list[str]] = UNSET,
    field_start: Union[Unset, int] = UNSET,
    field_end: Union[Unset, int] = UNSET,
    field_order: Union[Unset, EOrder] = UNSET,
    field_sort: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    gt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    gt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    fields: Union[Unset, list[str]] = UNSET,
) -> Response[Union[ProblemDetails, list["Monitoring"]]]:
    """Get list of object matching filter (Auth policies: ElementRead)

     Get list of object matching filter. Optionnal fields can be requested in the response by using
    fields query parameters

    Args:
        mon_connection_status (Union[Unset, str]):
        mon_type (Union[Unset, str]):
        mon_ip_address (Union[Unset, str]):
        monitoring_id (Union[Unset, list[int]]):
        mon_status (Union[Unset, str]):
        loc_country (Union[Unset, str]):
        loc_region (Union[Unset, str]):
        loc_province (Union[Unset, str]):
        loc_city (Union[Unset, str]):
        loc_group_1 (Union[Unset, str]):
        loc_group_2 (Union[Unset, str]):
        loc_group_3 (Union[Unset, str]):
        loc_group_4 (Union[Unset, str]):
        loc_group_5 (Union[Unset, str]):
        loc_name (Union[Unset, str]):
        loc_info (Union[Unset, str]):
        loc_type (Union[Unset, int]):
        q_loc (Union[Unset, str]):
        id (Union[Unset, list[str]]):
        field_start (Union[Unset, int]):
        field_end (Union[Unset, int]):
        field_order (Union[Unset, EOrder]):
        field_sort (Union[Unset, str]):
        q (Union[Unset, str]):
        gt_modified_date_time (Union[Unset, datetime.datetime]):
        lt_modified_date_time (Union[Unset, datetime.datetime]):
        gt_created_date_time (Union[Unset, datetime.datetime]):
        lt_created_date_time (Union[Unset, datetime.datetime]):
        fields (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, list['Monitoring']]]
    """

    kwargs = _get_kwargs(
        mon_connection_status=mon_connection_status,
        mon_type=mon_type,
        mon_ip_address=mon_ip_address,
        monitoring_id=monitoring_id,
        mon_status=mon_status,
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
        id=id,
        field_start=field_start,
        field_end=field_end,
        field_order=field_order,
        field_sort=field_sort,
        q=q,
        gt_modified_date_time=gt_modified_date_time,
        lt_modified_date_time=lt_modified_date_time,
        gt_created_date_time=gt_created_date_time,
        lt_created_date_time=lt_created_date_time,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    mon_connection_status: Union[Unset, str] = UNSET,
    mon_type: Union[Unset, str] = UNSET,
    mon_ip_address: Union[Unset, str] = UNSET,
    monitoring_id: Union[Unset, list[int]] = UNSET,
    mon_status: Union[Unset, str] = UNSET,
    loc_country: Union[Unset, str] = UNSET,
    loc_region: Union[Unset, str] = UNSET,
    loc_province: Union[Unset, str] = UNSET,
    loc_city: Union[Unset, str] = UNSET,
    loc_group_1: Union[Unset, str] = UNSET,
    loc_group_2: Union[Unset, str] = UNSET,
    loc_group_3: Union[Unset, str] = UNSET,
    loc_group_4: Union[Unset, str] = UNSET,
    loc_group_5: Union[Unset, str] = UNSET,
    loc_name: Union[Unset, str] = UNSET,
    loc_info: Union[Unset, str] = UNSET,
    loc_type: Union[Unset, int] = UNSET,
    q_loc: Union[Unset, str] = UNSET,
    id: Union[Unset, list[str]] = UNSET,
    field_start: Union[Unset, int] = UNSET,
    field_end: Union[Unset, int] = UNSET,
    field_order: Union[Unset, EOrder] = UNSET,
    field_sort: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    gt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_modified_date_time: Union[Unset, datetime.datetime] = UNSET,
    gt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    lt_created_date_time: Union[Unset, datetime.datetime] = UNSET,
    fields: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[ProblemDetails, list["Monitoring"]]]:
    """Get list of object matching filter (Auth policies: ElementRead)

     Get list of object matching filter. Optionnal fields can be requested in the response by using
    fields query parameters

    Args:
        mon_connection_status (Union[Unset, str]):
        mon_type (Union[Unset, str]):
        mon_ip_address (Union[Unset, str]):
        monitoring_id (Union[Unset, list[int]]):
        mon_status (Union[Unset, str]):
        loc_country (Union[Unset, str]):
        loc_region (Union[Unset, str]):
        loc_province (Union[Unset, str]):
        loc_city (Union[Unset, str]):
        loc_group_1 (Union[Unset, str]):
        loc_group_2 (Union[Unset, str]):
        loc_group_3 (Union[Unset, str]):
        loc_group_4 (Union[Unset, str]):
        loc_group_5 (Union[Unset, str]):
        loc_name (Union[Unset, str]):
        loc_info (Union[Unset, str]):
        loc_type (Union[Unset, int]):
        q_loc (Union[Unset, str]):
        id (Union[Unset, list[str]]):
        field_start (Union[Unset, int]):
        field_end (Union[Unset, int]):
        field_order (Union[Unset, EOrder]):
        field_sort (Union[Unset, str]):
        q (Union[Unset, str]):
        gt_modified_date_time (Union[Unset, datetime.datetime]):
        lt_modified_date_time (Union[Unset, datetime.datetime]):
        gt_created_date_time (Union[Unset, datetime.datetime]):
        lt_created_date_time (Union[Unset, datetime.datetime]):
        fields (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, list['Monitoring']]
    """

    return (
        await asyncio_detailed(
            client=client,
            mon_connection_status=mon_connection_status,
            mon_type=mon_type,
            mon_ip_address=mon_ip_address,
            monitoring_id=monitoring_id,
            mon_status=mon_status,
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
            id=id,
            field_start=field_start,
            field_end=field_end,
            field_order=field_order,
            field_sort=field_sort,
            q=q,
            gt_modified_date_time=gt_modified_date_time,
            lt_modified_date_time=lt_modified_date_time,
            gt_created_date_time=gt_created_date_time,
            lt_created_date_time=lt_created_date_time,
            fields=fields,
        )
    ).parsed
