from datetime import datetime
from types import List, NamedTuple


class Stop(NamedTuple):
    loc_id: int
    time_at_loc: datetime.time


class Route:
    def __init__(
        self,
        graph,
        destinations: List[int],
        vehicle_speed: float = 18.0,
    ) -> None:
        for i in range(len(destinations) - 1):
            a = destinations[i]
            b = destinations[i + 1]
        # need to import the city graph and then
