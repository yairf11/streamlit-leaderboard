import functools
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple


@functools.total_ordering
class Metric(ABC):
    def __init__(self, value: float):
        self.value = value

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def higher_is_better(cls) -> bool:
        pass

    def _check_other_metric_compatibility(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f"Comparing two different metrics: {type(other)} and {type(self)}")

    def __eq__(self, other):
        self._check_other_metric_compatibility(other)
        return other.value == self.value

    def __lt__(self, other):
        self._check_other_metric_compatibility(other)
        return (self.value < other.value) and self.higher_is_better


class Evaluator(ABC):
    def __init__(self, metrics: Tuple[Metric, ...]):
        self.metrics = metrics

    @abstractmethod
    def evaluate(self, filepath: Path) -> Tuple[Metric, ...]:
        pass
