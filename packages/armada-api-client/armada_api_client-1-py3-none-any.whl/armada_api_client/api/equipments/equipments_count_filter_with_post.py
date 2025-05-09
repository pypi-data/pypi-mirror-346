from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_details import ProblemDetails
from ...models.query_equipment import QueryEquipment
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        QueryEquipment,
        QueryEquipment,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Equipments/Count",
    }

    if isinstance(body, QueryEquipment):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, QueryEquipment):
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
        QueryEquipment,
        QueryEquipment,
    ],
) -> Response[Union[ProblemDetails, int]]:
    """Get the count of object filtered by query object in the post body (Auth policies: ElementRead)

    Args:
        body (QueryEquipment):
        body (QueryEquipment):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, int]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        QueryEquipment,
        QueryEquipment,
    ],
) -> Optional[Union[ProblemDetails, int]]:
    """Get the count of object filtered by query object in the post body (Auth policies: ElementRead)

    Args:
        body (QueryEquipment):
        body (QueryEquipment):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, int]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        QueryEquipment,
        QueryEquipment,
    ],
) -> Response[Union[ProblemDetails, int]]:
    """Get the count of object filtered by query object in the post body (Auth policies: ElementRead)

    Args:
        body (QueryEquipment):
        body (QueryEquipment):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, int]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        QueryEquipment,
        QueryEquipment,
    ],
) -> Optional[Union[ProblemDetails, int]]:
    """Get the count of object filtered by query object in the post body (Auth policies: ElementRead)

    Args:
        body (QueryEquipment):
        body (QueryEquipment):

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
        )
    ).parsed
