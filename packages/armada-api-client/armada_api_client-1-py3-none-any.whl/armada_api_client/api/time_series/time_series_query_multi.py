import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.e_aggregate import EAggregate
from ...models.multi_time_series import MultiTimeSeries
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    from_date_time: Union[Unset, datetime.datetime] = UNSET,
    to_date_time: Union[Unset, datetime.datetime] = UNSET,
    key: Union[Unset, list[str]] = UNSET,
    interval: Union[Unset, str] = UNSET,
    aggregate: Union[Unset, list[EAggregate]] = UNSET,
    create_empty: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_from_date_time: Union[Unset, str] = UNSET
    if not isinstance(from_date_time, Unset):
        json_from_date_time = from_date_time.isoformat()
    params["fromDateTime"] = json_from_date_time

    json_to_date_time: Union[Unset, str] = UNSET
    if not isinstance(to_date_time, Unset):
        json_to_date_time = to_date_time.isoformat()
    params["toDateTime"] = json_to_date_time

    json_key: Union[Unset, list[str]] = UNSET
    if not isinstance(key, Unset):
        json_key = key

    params["key"] = json_key

    params["interval"] = interval

    json_aggregate: Union[Unset, list[str]] = UNSET
    if not isinstance(aggregate, Unset):
        json_aggregate = []
        for aggregate_item_data in aggregate:
            aggregate_item = aggregate_item_data.value
            json_aggregate.append(aggregate_item)

    params["aggregate"] = json_aggregate

    params["createEmpty"] = create_empty

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/TimeSeries/queryMulti",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[MultiTimeSeries, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = MultiTimeSeries.from_dict(response.json())

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
) -> Response[Union[MultiTimeSeries, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    from_date_time: Union[Unset, datetime.datetime] = UNSET,
    to_date_time: Union[Unset, datetime.datetime] = UNSET,
    key: Union[Unset, list[str]] = UNSET,
    interval: Union[Unset, str] = UNSET,
    aggregate: Union[Unset, list[EAggregate]] = UNSET,
    create_empty: Union[Unset, bool] = UNSET,
) -> Response[Union[MultiTimeSeries, ProblemDetails]]:
    """(Auth policies: ElementRead)

    Args:
        from_date_time (Union[Unset, datetime.datetime]):
        to_date_time (Union[Unset, datetime.datetime]):
        key (Union[Unset, list[str]]):
        interval (Union[Unset, str]):
        aggregate (Union[Unset, list[EAggregate]]):
        create_empty (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[MultiTimeSeries, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        key=key,
        interval=interval,
        aggregate=aggregate,
        create_empty=create_empty,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    from_date_time: Union[Unset, datetime.datetime] = UNSET,
    to_date_time: Union[Unset, datetime.datetime] = UNSET,
    key: Union[Unset, list[str]] = UNSET,
    interval: Union[Unset, str] = UNSET,
    aggregate: Union[Unset, list[EAggregate]] = UNSET,
    create_empty: Union[Unset, bool] = UNSET,
) -> Optional[Union[MultiTimeSeries, ProblemDetails]]:
    """(Auth policies: ElementRead)

    Args:
        from_date_time (Union[Unset, datetime.datetime]):
        to_date_time (Union[Unset, datetime.datetime]):
        key (Union[Unset, list[str]]):
        interval (Union[Unset, str]):
        aggregate (Union[Unset, list[EAggregate]]):
        create_empty (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[MultiTimeSeries, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        key=key,
        interval=interval,
        aggregate=aggregate,
        create_empty=create_empty,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    from_date_time: Union[Unset, datetime.datetime] = UNSET,
    to_date_time: Union[Unset, datetime.datetime] = UNSET,
    key: Union[Unset, list[str]] = UNSET,
    interval: Union[Unset, str] = UNSET,
    aggregate: Union[Unset, list[EAggregate]] = UNSET,
    create_empty: Union[Unset, bool] = UNSET,
) -> Response[Union[MultiTimeSeries, ProblemDetails]]:
    """(Auth policies: ElementRead)

    Args:
        from_date_time (Union[Unset, datetime.datetime]):
        to_date_time (Union[Unset, datetime.datetime]):
        key (Union[Unset, list[str]]):
        interval (Union[Unset, str]):
        aggregate (Union[Unset, list[EAggregate]]):
        create_empty (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[MultiTimeSeries, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        key=key,
        interval=interval,
        aggregate=aggregate,
        create_empty=create_empty,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    from_date_time: Union[Unset, datetime.datetime] = UNSET,
    to_date_time: Union[Unset, datetime.datetime] = UNSET,
    key: Union[Unset, list[str]] = UNSET,
    interval: Union[Unset, str] = UNSET,
    aggregate: Union[Unset, list[EAggregate]] = UNSET,
    create_empty: Union[Unset, bool] = UNSET,
) -> Optional[Union[MultiTimeSeries, ProblemDetails]]:
    """(Auth policies: ElementRead)

    Args:
        from_date_time (Union[Unset, datetime.datetime]):
        to_date_time (Union[Unset, datetime.datetime]):
        key (Union[Unset, list[str]]):
        interval (Union[Unset, str]):
        aggregate (Union[Unset, list[EAggregate]]):
        create_empty (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[MultiTimeSeries, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            from_date_time=from_date_time,
            to_date_time=to_date_time,
            key=key,
            interval=interval,
            aggregate=aggregate,
            create_empty=create_empty,
        )
    ).parsed
