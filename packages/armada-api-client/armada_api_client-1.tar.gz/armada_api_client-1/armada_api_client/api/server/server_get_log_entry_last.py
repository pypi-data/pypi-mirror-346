from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_details import ProblemDetails
from ...models.server_log_entry import ServerLogEntry
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    last_qt: int,
    level_filter: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["lastQt"] = last_qt

    params["levelFilter"] = level_filter

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Server/GetLogEntryLast",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ProblemDetails, list["ServerLogEntry"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ServerLogEntry.from_dict(response_200_item_data)

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
) -> Response[Union[ProblemDetails, list["ServerLogEntry"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    last_qt: int,
    level_filter: Union[Unset, str] = UNSET,
) -> Response[Union[ProblemDetails, list["ServerLogEntry"]]]:
    """(Auth policies: AdminRead)

    Args:
        last_qt (int):
        level_filter (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, list['ServerLogEntry']]]
    """

    kwargs = _get_kwargs(
        last_qt=last_qt,
        level_filter=level_filter,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    last_qt: int,
    level_filter: Union[Unset, str] = UNSET,
) -> Optional[Union[ProblemDetails, list["ServerLogEntry"]]]:
    """(Auth policies: AdminRead)

    Args:
        last_qt (int):
        level_filter (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, list['ServerLogEntry']]
    """

    return sync_detailed(
        client=client,
        last_qt=last_qt,
        level_filter=level_filter,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    last_qt: int,
    level_filter: Union[Unset, str] = UNSET,
) -> Response[Union[ProblemDetails, list["ServerLogEntry"]]]:
    """(Auth policies: AdminRead)

    Args:
        last_qt (int):
        level_filter (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, list['ServerLogEntry']]]
    """

    kwargs = _get_kwargs(
        last_qt=last_qt,
        level_filter=level_filter,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    last_qt: int,
    level_filter: Union[Unset, str] = UNSET,
) -> Optional[Union[ProblemDetails, list["ServerLogEntry"]]]:
    """(Auth policies: AdminRead)

    Args:
        last_qt (int):
        level_filter (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, list['ServerLogEntry']]
    """

    return (
        await asyncio_detailed(
            client=client,
            last_qt=last_qt,
            level_filter=level_filter,
        )
    ).parsed
