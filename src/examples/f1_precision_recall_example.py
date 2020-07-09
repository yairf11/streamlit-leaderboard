import json
from pathlib import Path
from typing import Tuple, Type
import numpy as np
from sklearn.metrics import precision_recall_fscore_support

from src.examples.generate_predictions import GROUND_TRUTH_DATA
from src.evaluator import Metric, Evaluator


class F1(Metric):
    @classmethod
    def name(cls) -> str:
        return 'F1'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class Precision(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Precision'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class Recall(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Recall'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class ExampleEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
        self.true_label_dict = GROUND_TRUTH_DATA
        self.labels_array = np.array(list(self.true_label_dict.values()))

    @classmethod
    def metrics(cls) -> Tuple[Type[Metric], ...]:
        return (F1, Precision, Recall)

    def validate_submission_return_error_message(self, filepath: Path) -> str:
        try:
            with filepath.open('r') as f:
                predictions = json.load(f)
        except:
            return 'Problem while loading file.'
        if type(predictions) != dict:
            return 'Submission is not in the correct format.'
        if set(predictions) != set(self.true_label_dict):
            return 'Submission prediction ids not as expected.'
        return ''

    def evaluate(self, filepath: Path) -> Tuple[Metric, ...]:
        with filepath.open('r') as f:
            predictions = json.load(f)
        preds_array = np.array([predictions.get(k, 1-self.true_label_dict[k])
                                for k in self.true_label_dict.keys()])
        precision, recall, f1, _ = precision_recall_fscore_support(y_true=self.labels_array,
                                                                   y_pred=preds_array)
        return (F1(f1), Precision(precision), Recall(recall))