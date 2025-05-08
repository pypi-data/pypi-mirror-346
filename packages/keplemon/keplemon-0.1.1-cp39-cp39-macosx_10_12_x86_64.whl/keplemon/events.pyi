# flake8: noqa
from keplemon.time import Epoch

class CloseApproach:
    epoch: Epoch
    primary_id: int
    secondary_id: int
    distance: float

class CloseApproachReport:
    close_approaches: list[CloseApproach]
    distance_threshold: float
