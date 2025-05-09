import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.e_order import EOrder
from ...models.problem_details import ProblemDetails
from ...models.report_info import ReportInfo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    report_id: Union[Unset, list[int]] = UNSET,
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

    json_report_id: Union[Unset, list[int]] = UNSET
    if not isinstance(report_id, Unset):
        json_report_id = report_id

    params["reportId"] = json_report_id

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
        "url": "/api/Reports",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ProblemDetails, list["ReportInfo"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ReportInfo.from_dict(response_200_item_data)

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
) -> Response[Union[ProblemDetails, list["ReportInfo"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    report_id: Union[Unset, list[int]] = UNSET,
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
) -> Response[Union[ProblemDetails, list["ReportInfo"]]]:
    """Get list of object matching filter (Auth policies: ReportRead)

     Get list of object matching filter. Optionnal fields can be requested in the response by using
    fields query parameters

    Args:
        report_id (Union[Unset, list[int]]):
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
        Response[Union[ProblemDetails, list['ReportInfo']]]
    """

    kwargs = _get_kwargs(
        report_id=report_id,
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
    report_id: Union[Unset, list[int]] = UNSET,
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
) -> Optional[Union[ProblemDetails, list["ReportInfo"]]]:
    """Get list of object matching filter (Auth policies: ReportRead)

     Get list of object matching filter. Optionnal fields can be requested in the response by using
    fields query parameters

    Args:
        report_id (Union[Unset, list[int]]):
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
        Union[ProblemDetails, list['ReportInfo']]
    """

    return sync_detailed(
        client=client,
        report_id=report_id,
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
    report_id: Union[Unset, list[int]] = UNSET,
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
) -> Response[Union[ProblemDetails, list["ReportInfo"]]]:
    """Get list of object matching filter (Auth policies: ReportRead)

     Get list of object matching filter. Optionnal fields can be requested in the response by using
    fields query parameters

    Args:
        report_id (Union[Unset, list[int]]):
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
        Response[Union[ProblemDetails, list['ReportInfo']]]
    """

    kwargs = _get_kwargs(
        report_id=report_id,
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
    report_id: Union[Unset, list[int]] = UNSET,
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
) -> Optional[Union[ProblemDetails, list["ReportInfo"]]]:
    """Get list of object matching filter (Auth policies: ReportRead)

     Get list of object matching filter. Optionnal fields can be requested in the response by using
    fields query parameters

    Args:
        report_id (Union[Unset, list[int]]):
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
        Union[ProblemDetails, list['ReportInfo']]
    """

    return (
        await asyncio_detailed(
            client=client,
            report_id=report_id,
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
