from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_details import ProblemDetails
from ...models.query_monitoring import QueryMonitoring
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: Union[
        QueryMonitoring,
        QueryMonitoring,
    ],
    file_info_id: int,
    remote_directory: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["fileInfoId"] = file_info_id

    params["remoteDirectory"] = remote_directory

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/MonitoringFtpUploadJobs/CreateJobs",
        "params": params,
    }

    if isinstance(body, QueryMonitoring):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, QueryMonitoring):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/*+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ProblemDetails, int]]:
    if response.status_code == 200:
        response_200 = cast(int, response.json())
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
) -> Response[Union[ProblemDetails, int]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        QueryMonitoring,
        QueryMonitoring,
    ],
    file_info_id: int,
    remote_directory: str,
) -> Response[Union[ProblemDetails, int]]:
    """(Auth policies: AdminRead, AdminWrite)

    Args:
        file_info_id (int):
        remote_directory (str):
        body (QueryMonitoring):
        body (QueryMonitoring):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, int]]
    """

    kwargs = _get_kwargs(
        body=body,
        file_info_id=file_info_id,
        remote_directory=remote_directory,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        QueryMonitoring,
        QueryMonitoring,
    ],
    file_info_id: int,
    remote_directory: str,
) -> Optional[Union[ProblemDetails, int]]:
    """(Auth policies: AdminRead, AdminWrite)

    Args:
        file_info_id (int):
        remote_directory (str):
        body (QueryMonitoring):
        body (QueryMonitoring):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, int]
    """

    return sync_detailed(
        client=client,
        body=body,
        file_info_id=file_info_id,
        remote_directory=remote_directory,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        QueryMonitoring,
        QueryMonitoring,
    ],
    file_info_id: int,
    remote_directory: str,
) -> Response[Union[ProblemDetails, int]]:
    """(Auth policies: AdminRead, AdminWrite)

    Args:
        file_info_id (int):
        remote_directory (str):
        body (QueryMonitoring):
        body (QueryMonitoring):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, int]]
    """

    kwargs = _get_kwargs(
        body=body,
        file_info_id=file_info_id,
        remote_directory=remote_directory,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        QueryMonitoring,
        QueryMonitoring,
    ],
    file_info_id: int,
    remote_directory: str,
) -> Optional[Union[ProblemDetails, int]]:
    """(Auth policies: AdminRead, AdminWrite)

    Args:
        file_info_id (int):
        remote_directory (str):
        body (QueryMonitoring):
        body (QueryMonitoring):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, int]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            file_info_id=file_info_id,
            remote_directory=remote_directory,
        )
    ).parsed
