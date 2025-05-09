from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.e_control_service import EControlService
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    wanted_state: Union[Unset, EControlService] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_wanted_state: Union[Unset, str] = UNSET
    if not isinstance(wanted_state, Unset):
        json_wanted_state = wanted_state.value

    params["wantedState"] = json_wanted_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Nodered/ServiceControl",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ProblemDetails, bool]]:
    if response.status_code == 200:
        response_200 = cast(bool, response.json())
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
) -> Response[Union[ProblemDetails, bool]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    wanted_state: Union[Unset, EControlService] = UNSET,
) -> Response[Union[ProblemDetails, bool]]:
    """(Auth policies: NoderedAdmin)

    Args:
        wanted_state (Union[Unset, EControlService]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, bool]]
    """

    kwargs = _get_kwargs(
        wanted_state=wanted_state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    wanted_state: Union[Unset, EControlService] = UNSET,
) -> Optional[Union[ProblemDetails, bool]]:
    """(Auth policies: NoderedAdmin)

    Args:
        wanted_state (Union[Unset, EControlService]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, bool]
    """

    return sync_detailed(
        client=client,
        wanted_state=wanted_state,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    wanted_state: Union[Unset, EControlService] = UNSET,
) -> Response[Union[ProblemDetails, bool]]:
    """(Auth policies: NoderedAdmin)

    Args:
        wanted_state (Union[Unset, EControlService]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, bool]]
    """

    kwargs = _get_kwargs(
        wanted_state=wanted_state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    wanted_state: Union[Unset, EControlService] = UNSET,
) -> Optional[Union[ProblemDetails, bool]]:
    """(Auth policies: NoderedAdmin)

    Args:
        wanted_state (Union[Unset, EControlService]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, bool]
    """

    return (
        await asyncio_detailed(
            client=client,
            wanted_state=wanted_state,
        )
    ).parsed
