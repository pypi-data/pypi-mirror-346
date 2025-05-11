from datetime import datetime
from http import HTTPStatus
import asyncio

import aiohttp

from weiche.api.base import BaseApi
from weiche.api.parser import parse_associations, parse_connection_response, parse_locations
from weiche.const import DEFAULT_BASE_URL
from weiche.objects import Association, Connection, ConnectionRequest, Location


class AsynchronousApi(BaseApi):
    def __init__(self, base_url: str = DEFAULT_BASE_URL, proxy: str | None = None) -> None:
        super().__init__(base_url)
        proxy = proxy or None
        self.session = aiohttp.ClientSession(proxy=proxy)

    async def get_travel_associations(self) -> list[Association]:
        async with self.session.get(self.travel_associations_url) as response:
            assert response.status == HTTPStatus.OK, f"Error: {response.status}"
            return parse_associations(await response.json())

    async def search_locations(self, query: str, limit: int = 10, location_type: str = "ALL") -> list[Location]:
        tries = 0
        while True:
            async with self.session.get(
                self.locations_url,
                params=self.get_locations_params(
                    query=query,
                    limit=limit,
                    location_type=location_type,
                ),
            ) as response:
                if response.status == HTTPStatus.TOO_MANY_REQUESTS:
                    tries += 1
                    await asyncio.sleep(tries)
                    continue

                assert response.status == HTTPStatus.OK, f"Error: {response.status}"
                return parse_locations(await response.json())

    async def search_connections(
        self,
        at: datetime,
        from_location: str,
        to_location: str,
        limit: int = 10,
    ) -> list[Connection]:
        return await self.search_connections_ext(
            self.get_connections_request_from_params(from_location, to_location, at),
            limit=limit,
        )

    async def search_connections_ext(self, request: ConnectionRequest, limit: int = 10) -> list[Connection]:
        responses: list[Connection] = []
        tries = 0
        while len(responses) < limit:
            request_params = self.get_connections_ext_params(request)
            async with self.session.post(
                self.connections_url,
                json=request_params,
            ) as response:
                if response.status == HTTPStatus.TOO_MANY_REQUESTS:
                    tries += 1
                    await asyncio.sleep(tries)
                    continue
                tries = 0

                assert response.status in (
                    HTTPStatus.OK,
                    HTTPStatus.CREATED,
                ), f"Error: {response.status}, {await response.text()}"
                connection_response = parse_connection_response(await response.json())
                responses.extend(connection_response.connections)
            if limit and len(responses) > limit:
                responses = responses[:limit]

            if not connection_response.has_more:
                break

            request.paging_reference = connection_response.next_pointer

        return responses
