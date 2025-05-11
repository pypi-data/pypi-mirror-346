from datetime import datetime

import pytest

from weiche import Schiene


@pytest.mark.parametrize("only_direct", [True, False])
def test_connections_api(only_direct: bool) -> None:
    api = Schiene()
    response = api.connections("München Hbf", "Berlin Hbf", dt=datetime.now(), only_direct=True)
    assert len(response) > 0


def test_stations_api() -> None:
    api = Schiene()
    response = api.stations("München Hbf", limit=1)
    assert len(response) == 1
    assert response[0]["prodClass"] == "ICE,EC_IC,IR,REGIONAL,SBAHN,BUS,UBAHN,TRAM"
