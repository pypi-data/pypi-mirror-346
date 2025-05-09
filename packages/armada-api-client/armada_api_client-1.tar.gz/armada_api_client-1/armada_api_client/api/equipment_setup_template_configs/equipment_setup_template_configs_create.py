from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.equipment_setup_template_config import EquipmentSetupTemplateConfig
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        EquipmentSetupTemplateConfig,
        EquipmentSetupTemplateConfig,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/EquipmentSetupTemplateConfigs",
    }

    if isinstance(body, EquipmentSetupTemplateConfig):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, EquipmentSetupTemplateConfig):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/*+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[EquipmentSetupTemplateConfig, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = EquipmentSetupTemplateConfig.from_dict(response.json())

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
) -> Response[Union[EquipmentSetupTemplateConfig, ProblemDetails]]:
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
        EquipmentSetupTemplateConfig,
        EquipmentSetupTemplateConfig,
    ],
) -> Response[Union[EquipmentSetupTemplateConfig, ProblemDetails]]:
    """(Auth policies: AdminWrite)

    Args:
        body (EquipmentSetupTemplateConfig):
        body (EquipmentSetupTemplateConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EquipmentSetupTemplateConfig, ProblemDetails]]
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
        EquipmentSetupTemplateConfig,
        EquipmentSetupTemplateConfig,
    ],
) -> Optional[Union[EquipmentSetupTemplateConfig, ProblemDetails]]:
    """(Auth policies: AdminWrite)

    Args:
        body (EquipmentSetupTemplateConfig):
        body (EquipmentSetupTemplateConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EquipmentSetupTemplateConfig, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        EquipmentSetupTemplateConfig,
        EquipmentSetupTemplateConfig,
    ],
) -> Response[Union[EquipmentSetupTemplateConfig, ProblemDetails]]:
    """(Auth policies: AdminWrite)

    Args:
        body (EquipmentSetupTemplateConfig):
        body (EquipmentSetupTemplateConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EquipmentSetupTemplateConfig, ProblemDetails]]
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
        EquipmentSetupTemplateConfig,
        EquipmentSetupTemplateConfig,
    ],
) -> Optional[Union[EquipmentSetupTemplateConfig, ProblemDetails]]:
    """(Auth policies: AdminWrite)

    Args:
        body (EquipmentSetupTemplateConfig):
        body (EquipmentSetupTemplateConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EquipmentSetupTemplateConfig, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
