from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

@dataclass
class Flight:
    '''
        launch: A Launch instance for this flight
        launchtime: Datetime of launch
        distance: Distance in kilometers
    '''

    launch: Launch
    launchtime: datetime
    distance: float


@dataclass
class Launch:
    '''
    launchname: Launchsite name string, given by pilot
    coordinates: (DD, DD) (https://en.wikipedia.org/wiki/Decimal_degrees)
    official: Whether this launch site has been recognized as official launch site or not
    '''

    launchname: str
    coordinates: Tuple[float, float]
    registered: bool

    def latitude(self):

        return self.coordinates[0]

    def longitude(self):

        return self.coordinates[1]
