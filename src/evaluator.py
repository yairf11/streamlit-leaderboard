import functools
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple


@functools.total_ordering
class Metric:
    def __init__(self, name: str, value: float, higher_is_better: bool):
        self.name = name
        self.value = value
        self.higher_is_better = higher_is_better

    def _check_other_metric_compatibility(self, other):
        if other.name != self.name or other.higer_is_better != self.higher_is_better:
            raise TypeError(f"Comparing two different metrics: {self.name} and {other.name}")

    def __eq__(self, other):
        self._check_other_metric_compatibility(other)
        return other.value == self.value

    def __lt__(self, other):
        self._check_other_metric_compatibility(other)
        return (self.value < other.value) and self.higher_is_better


class Evaluator(ABC):
    def __init__(self, ground_truth_file: Path):
        self.ground_truth_file = ground_truth_file

    @abstractmethod
    def evaluate(self) -> Tuple[Metric]:
        pass
