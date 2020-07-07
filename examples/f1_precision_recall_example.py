from src.evaluator import Metric


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


random_data
