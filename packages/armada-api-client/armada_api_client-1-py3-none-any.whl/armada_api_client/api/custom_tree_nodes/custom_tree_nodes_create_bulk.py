from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.custom_tree_node import CustomTreeNode
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        list["CustomTreeNode"],
        list["CustomTreeNode"],
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/CustomTreeNodes/AddList",
    }

    if isinstance(body, list["CustomTreeNode"]):
        _json_body = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _json_body.append(body_item)

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, list["CustomTreeNode"]):
        _json_body = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _json_body.append(body_item)

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/*+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ProblemDetails, list["CustomTreeNode"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = CustomTreeNode.from_dict(response_200_item_data)

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
) -> Response[Union[ProblemDetails, list["CustomTreeNode"]]]:
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
        list["CustomTreeNode"],
        list["CustomTreeNode"],
    ],
) -> Response[Union[ProblemDetails, list["CustomTreeNode"]]]:
    """(Auth policies: LocationRead, LocationWrite)

    Args:
        body (list['CustomTreeNode']):
        body (list['CustomTreeNode']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, list['CustomTreeNode']]]
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
        list["CustomTreeNode"],
        list["CustomTreeNode"],
    ],
) -> Optional[Union[ProblemDetails, list["CustomTreeNode"]]]:
    """(Auth policies: LocationRead, LocationWrite)

    Args:
        body (list['CustomTreeNode']):
        body (list['CustomTreeNode']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, list['CustomTreeNode']]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list["CustomTreeNode"],
        list["CustomTreeNode"],
    ],
) -> Response[Union[ProblemDetails, list["CustomTreeNode"]]]:
    """(Auth policies: LocationRead, LocationWrite)

    Args:
        body (list['CustomTreeNode']):
        body (list['CustomTreeNode']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProblemDetails, list['CustomTreeNode']]]
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
        list["CustomTreeNode"],
        list["CustomTreeNode"],
    ],
) -> Optional[Union[ProblemDetails, list["CustomTreeNode"]]]:
    """(Auth policies: LocationRead, LocationWrite)

    Args:
        body (list['CustomTreeNode']):
        body (list['CustomTreeNode']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProblemDetails, list['CustomTreeNode']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
