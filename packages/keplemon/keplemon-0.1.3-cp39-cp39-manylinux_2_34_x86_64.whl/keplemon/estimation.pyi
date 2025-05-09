# flake8: noqa
from keplemon.elements import TopocentricElements, CartesianVector
from keplemon.time import Epoch
from keplemon.bodies import Satellite, Sensor
from keplemon.enums import KeplerianType

class Covariance:
    sigmas: list[float]

class Observation:
    def __init__(
        self,
        sensor: Sensor,
        epoch: Epoch,
        observed_teme_topo: TopocentricElements,
        observer_teme_pos: CartesianVector,
    ) -> None: ...
    def get_residual(self, sat: Satellite) -> ObservationResidual: ...

class ObservationResidual:
    range: float
    radial: float
    in_track: float
    cross_track: float
    time: float
    beta: float

class BatchLeastSquares:
    converged: bool
    max_iterations: int
    iteration_count: int
    current_estimate: Satellite
    rms: float | None
    weighted_rms: float | None
    estimate_srp: bool
    estimate_drag: bool
    a_priori: Satellite
    observations: list[Observation]
    residuals: list[tuple[Epoch, ObservationResidual]]
    covariance: Covariance | None
    output_type: KeplerianType
    def __init__(
        self,
        obs: list[Observation],
        a_priori: Satellite,
    ) -> None: ...
    def solve(self) -> None: ...
