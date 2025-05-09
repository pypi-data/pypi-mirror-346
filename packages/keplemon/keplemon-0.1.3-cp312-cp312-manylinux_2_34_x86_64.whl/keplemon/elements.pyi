# flake8: noqa
from __future__ import annotations
from keplemon.time import Epoch
from keplemon.enums import Classification, KeplerianType, ReferenceFrame
from keplemon.propagation import ForceProperties
from keplemon.events import CloseApproach

class KeplerianElements:
    semi_major_axis: float
    eccentricity: float
    inclination: float
    raan: float
    argument_of_perigee: float
    mean_anomaly: float

    def __init__(
        self,
        semi_major_axis: float,
        eccentricity: float,
        inclination: float,
        raan: float,
        argument_of_perigee: float,
        mean_anomaly: float,
    ) -> None: ...

class TLE:
    satellite_id: int
    designator: str
    classification: Classification
    keplerian_state: KeplerianState
    force_properties: ForceProperties
    ephemeris_type: KeplerianType

    @classmethod
    def from_lines(cls, line_1: str, line_2: str, line_3: str | None = None) -> TLE: ...
    def get_lines(self) -> tuple[str, str]: ...
    def load_to_memory(self) -> None: ...
    def get_state_at_epoch(self, epoch: Epoch) -> CartesianState: ...

class SphericalVector:
    range: float
    right_ascension: float
    declination: float
    def __init__(self, range: float, right_ascension: float, declination: float) -> None: ...
    def to_cartesian(self) -> CartesianVector: ...

class CartesianVector:
    x: float
    y: float
    z: float
    magnitude: float
    def __init__(self, x: float, y: float, z: float) -> None: ...
    def distance(self, other: CartesianVector) -> float: ...
    def to_spherical(self) -> SphericalVector: ...
    def __add__(self, other: CartesianVector) -> CartesianVector: ...
    def __sub__(self, other: CartesianVector) -> CartesianVector: ...
    def angle(self, other: CartesianVector) -> float: ...

class CartesianState:
    position: CartesianVector
    velocity: CartesianVector

class KeplerianState:
    epoch: Epoch
    elements: KeplerianElements
    frame: ReferenceFrame
    keplerian_type: KeplerianType
    def __init__(
        self,
        epoch: Epoch,
        elements: KeplerianElements,
        frame: ReferenceFrame,
        keplerian_type: KeplerianType,
    ) -> None: ...

class Ephemeris:
    def get_close_approach(
        self,
        other: Ephemeris,
        distance_threshold: float,
    ) -> CloseApproach: ...

class TopocentricElements:
    range: float | None
    right_ascension: float
    declination: float
    range_rate: float | None
    right_ascension_rate: float | None
    declination_rate: float | None
    def __init__(self, ra: float, dec: float) -> None: ...
    @classmethod
    def from_j2000(cls, epoch: Epoch, ra: float, dec: float) -> TopocentricElements: ...
