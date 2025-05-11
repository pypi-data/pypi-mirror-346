from datetime import datetime

import pytest

from weiche import SynchronousApi


def test_connections_api() -> None:
    api = SynchronousApi()
    munich_locations = api.search_locations("München Hbf", limit=1)
    assert len(munich_locations) == 1
    munich = munich_locations[0]

    berlin_locations = api.search_locations("Berlin Hbf", limit=1)
    assert len(berlin_locations) == 1
    berlin = berlin_locations[0]

    connections = api.search_connections(
        at=datetime.now(),
        from_location=munich.id,
        to_location=berlin.id,
        limit=10,
    )
    assert len(connections) == 10


@pytest.mark.parametrize("target", ["Amsterdam", "Wien Hbf", "Paris", "London"])
def test_connections_api_international(target: str) -> None:
    api = SynchronousApi()
    munich_locations = api.search_locations("München Hbf", limit=1)
    assert len(munich_locations) == 1
    munich = munich_locations[0]

    target_locations = api.search_locations(target, limit=1)
    assert len(target_locations) == 1
    target_obj = target_locations[0]

    connections = api.search_connections(
        at=datetime(2025, 5, 10, 18, 0, 0),
        from_location=munich.id,
        to_location=target_obj.id,
    )
    assert len(connections) > 0
