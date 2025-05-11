from typing import Any

from pydantic import RootModel

from weiche.objects import Association, ConnectionResponse, Location


def parse_locations(payload: list[Any]) -> list[Location]:
    return RootModel[list[Location]].model_validate(payload, by_alias=True).root


def parse_connection_response(payload: dict[str, Any]) -> ConnectionResponse:
    return ConnectionResponse.model_validate(payload, by_alias=True)


def parse_associations(payload: list[Any]) -> list[Association]:
    return RootModel[list[Association]].model_validate(payload, by_alias=True).root
