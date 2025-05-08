# flake8: noqa
from keplemon.elements import TLE, CartesianState, Ephemeris
from keplemon.catalogs import TLECatalog
from keplemon.time import Epoch, TimeSpan
from keplemon.events import CloseApproach, CloseApproachReport

class Earth:
    @staticmethod
    def get_equatorial_radius() -> float: ...
    @staticmethod
    def get_kem() -> float: ...

class Satellite:
    satellite_id: int
    name: str | None
    @classmethod
    def from_tle(cls, tle: TLE) -> Satellite: ...
    def get_close_approach(
        self,
        other: Satellite,
        start: Epoch,
        end: Epoch,
        distance_threshold: float,
    ) -> None | CloseApproach: ...
    def get_ephemeris(
        self,
        start: Epoch,
        end: Epoch,
        step: TimeSpan,
    ) -> Ephemeris: ...
    def get_state_at_epoch(self, epoch: Epoch) -> CartesianState: ...

class Constellation:
    count: int
    name: str | None
    def __init__(self, name: str) -> None: ...
    @classmethod
    def from_tle_catalog(cls, tle_catalog: TLECatalog) -> Constellation: ...
    def get_states_at_epoch(self, epoch: Epoch) -> dict[str, CartesianState]: ...
    def get_ephemeris(
        self,
        start: Epoch,
        end: Epoch,
        step: TimeSpan,
    ) -> dict[str, Ephemeris]: ...
    def get_ca_report_vs_one(
        self,
        other: Satellite,
        start: Epoch,
        end: Epoch,
        distance_threshold: float,
    ) -> CloseApproachReport: ...
    def get_ca_report_vs_many(
        self,
        start: Epoch,
        end: Epoch,
        distance_threshold: float,
    ) -> CloseApproachReport: ...

class Sensor:
    name: str
    angular_noise: float
    range_noise: float
    range_rate_noise: float
    angular_rate_noise: float
    def __init__(self, name: str, angular_noise: float) -> None: ...

class Observatory:
    name: str
    latitude: float
    longitude: float
    altitude: float
    sensors: list[Sensor]
    def __init__(
        self,
        name: str,
        latitude: float,
        longitude: float,
        altitude: float,
    ) -> None: ...
    def get_state_at_epoch(self, epoch: Epoch) -> CartesianState: ...
