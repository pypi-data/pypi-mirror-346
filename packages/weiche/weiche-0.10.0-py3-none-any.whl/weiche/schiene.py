from datetime import datetime
from typing import TypedDict

from weiche.api.synchronous import SynchronousApi
from weiche.objects import Connection, Location


class SchieneStation(TypedDict):
    extId: str
    id: str
    prodClass: str
    state: str
    type: str
    typeStr: str
    value: str
    weight: str
    xcoord: str
    ycoord: str


class SchieneConnectionDelay(TypedDict):
    delay_arrival: int
    delay_departure: int


class SchieneConnection(TypedDict):
    arrival: str
    canceled: bool
    departure: str
    delay: SchieneConnectionDelay | None
    details: str
    price: float | None
    products: list[str]
    time: str
    transfers: int
    ontime: bool


def datetime_to_time_string(dt: datetime | None) -> str:
    if dt is None:
        return ""
    return dt.strftime("%H:%M")


def connection_to_dict(connection: Connection) -> SchieneConnection:
    if connection.price is None:
        amount = None
    else:
        amount = connection.price.amount

    payload = SchieneConnection(
        arrival=datetime_to_time_string(connection.planned_arrival_time),
        canceled=connection.cancelled,
        departure=datetime_to_time_string(connection.planned_departure_time),
        details="",
        price=amount,
        products=[
            segment.means_of_transport.product_type
            for segment in connection.segments
            if segment.means_of_transport.product_type
        ],
        time=connection.ez_connection_time_string or connection.connection_time_string,
        transfers=connection.changes,
        ontime=connection.on_time,
        delay=None,
    )
    if not connection.on_time:
        payload["delay"] = SchieneConnectionDelay(
            delay_departure=int(connection.delay_departure.total_seconds() // 60),
            delay_arrival=int(connection.delay_arrival.total_seconds() // 60),
        )
    return payload


def schiene_to_dict(location: Location, index: int) -> SchieneStation:
    return SchieneStation(
        extId=location.ext_id,
        id=location.id,
        prodClass=",".join(product for product in location.products if product),
        state="id",
        type=location.type,
        typeStr=location.type,
        value=location.name,
        weight=str(index),
        xcoord=str(int(location.lon * 1_000_000)),
        ycoord=str(int(location.lat * 1_000_000)),
    )


class Schiene:
    def __init__(self, proxy: str | None = None) -> None:
        self.api = SynchronousApi(proxy=proxy)

    def stations(self, station: str, limit: int = 10) -> list[SchieneStation]:
        """Find stations for given queries.

        Args:
            station (str): search query
            limit (int): limit number of results
        """
        stations = []
        locations = self.api.search_locations(station, limit=limit)
        for index, location in enumerate(locations):
            stations.append(schiene_to_dict(location, index))
        return stations

    def connections(
        self, origin: str, destination: str, dt: datetime = datetime.now(), only_direct: bool = False
    ) -> list[SchieneConnection]:
        """Find connections between two stations.

        Args:
            origin (str): origin station
            destination (str): destination station
            dt (datetime): date and time for query
            only_direct (bool): only direct connections
        """
        origin_locations = self.api.search_locations(origin, limit=1)
        if not origin_locations:
            return []
        origin_location = origin_locations[0]
        destination_locations = self.api.search_locations(destination, limit=1)
        if not destination_locations:
            return []
        destination_location = destination_locations[0]
        connections = self.api.search_connections(
            at=dt,
            from_location=origin_location.id,
            to_location=destination_location.id,
            limit=10,
        )
        if only_direct:
            connections = [c for c in connections if c.direct]

        return [connection_to_dict(c) for c in connections]
