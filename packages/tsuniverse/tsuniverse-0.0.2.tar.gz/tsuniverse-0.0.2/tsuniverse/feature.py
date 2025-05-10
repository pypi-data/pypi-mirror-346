"""The base class for a feature."""

from typing import NotRequired, TypedDict


class Feature(TypedDict):
    """A description of a feature to use."""

    predictor: str
    predictor_transform: str
    predictand: str
    predictand_transform: str
    lag: NotRequired[float]
    correlation: NotRequired[float]
