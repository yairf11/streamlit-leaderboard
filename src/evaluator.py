from abc import ABC, abstractmethod
from pathlib import Path


class Evaluator(ABC):
    def __init__(self, ground_truth_file: Path):
        self.ground_truth_file = ground_truth_file

    @abstractmethod
    def evaluate(self):
        pass