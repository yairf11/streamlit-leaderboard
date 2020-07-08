import json
from pathlib import Path
from typing import Tuple
import numpy as np
from sklearn.metrics import precision_recall_fscore_support

from examples.generate_predictions import GROUND_TRUTH_DATA
from src.evaluator import Metric, Evaluator


class F1(Metric):
    def name(cls) -> str:
        return 'F1'

    def higher_is_better(cls) -> bool:
        return True


class Precision(Metric):
    def name(cls) -> str:
        return 'Precision'

    def higher_is_better(cls) -> bool:
        return True


class Recall(Metric):
    def name(cls) -> str:
        return 'Recall'

    def higher_is_better(cls) -> bool:
        return True


class ExampleEvaluator(Evaluator):
    def __init__(self, metrics: Tuple[Metric, ...]):
        super().__init__(metrics)
        self.true_label_dict = GROUND_TRUTH_DATA
        self.labels_array = np.array(list(self.true_label_dict.values()))

    def evaluate(self, filepath: Path) -> Tuple[Metric, ...]:
        with filepath.open('r') as f:
            predictions = json.load(f)
        preds_array = np.array([predictions.get(k, 1-self.true_label_dict[k])
                                for k in self.true_label_dict.keys()])
        precision, recall, f1, _ = precision_recall_fscore_support(y_true=self.labels_array,
                                                                   y_pred=preds_array)
        return (Precision(precision), Recall(recall), F1(f1))
