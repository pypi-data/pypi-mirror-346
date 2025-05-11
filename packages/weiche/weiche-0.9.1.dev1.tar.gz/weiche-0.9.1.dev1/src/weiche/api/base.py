import json
from datetime import datetime
from typing import Any
from urllib.parse import urljoin

from weiche.const import DEFAULT_BASE_URL
from weiche.objects import ConnectionRequest


class BaseApi:
    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url

    @property
    def locations_url(self):
        return urljoin(self.base_url, "reiseloesung/orte")

    def get_locations_params(self, query: str, limit: int = 10, location_type: str = "ALL") -> dict[str, Any]:
        return {
            "suchbegriff": query,
            "typ": location_type,
            "limit": limit,
        }

    @property
    def connections_url(self):
        return urljoin(self.base_url, "angebote/fahrplan")

    def get_connections_request_from_params(
        self, from_location: str, to_location: str, at: datetime | None = None, paging_reference: str | None = None
    ) -> ConnectionRequest:
        at = at or datetime.now()
        return ConnectionRequest(
            time=at,
            origin=from_location,
            destination=to_location,
            paging_reference=paging_reference,
        )

    def get_connections_ext_params(self, request: ConnectionRequest) -> dict[str, Any]:
        request = request.model_copy()
        request.time = request.time.replace(tzinfo=None, microsecond=0)
        return json.loads(request.model_dump_json(by_alias=True, exclude_none=True))

    @property
    def travel_associations_url(self):
        return urljoin(self.base_url, "angebote/stammdaten/verbuende")
