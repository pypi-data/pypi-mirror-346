from datetime import datetime

import pytest

from weiche import AsynchronousApi


@pytest.mark.asyncio
async def test_connections_api() -> None:
    api = AsynchronousApi()
    munich_locations = await api.search_locations("München Hbf", limit=1)
    assert len(munich_locations) == 1
    munich = munich_locations[0]

    berlin_locations = await api.search_locations("Berlin Hbf", limit=1)
    assert len(berlin_locations) == 1
    berlin = berlin_locations[0]

    connections = await api.search_connections(
        at=datetime.now(),
        from_location=munich.id,
        to_location=berlin.id,
        limit=10,
    )
    assert len(connections) == 10
