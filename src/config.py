from pathlib import Path

from src.examples.f1_precision_recall_example import ExampleEvaluator

SUBMISSIONS_DIR = Path(__file__).parent.parent.absolute() / 'submissions'
PASSWORDS_FILE = Path(__file__).parent.parent.absolute() / 'passwords.json'
ARGON2_KWARGS = {}

EVALUATOR_CLASS = ExampleEvaluator
EVALUATOR_KWARGS = {}