from io import BytesIO, StringIO
from pathlib import Path
from typing import List, Callable, Tuple, Dict, Union

from src.evaluator import Metric


class SingleParticipantSubmissions:
    def __init__(self, participant_submission_dir: Path, evaluator: Callable[[Path], Tuple[Metric]]):
        self.participant_submission_dir = participant_submission_dir
        self.participant_name = self.participant_submission_dir.parts[-1]
        self.evaluator = evaluator
        self.results : Dict[Path: Tuple[Metric]] = dict()

    def get_submissions(self) -> List[Path]:
        return [x for x in self.participant_submission_dir.iterdir() if x.is_file()]

    def add_submission(self, io_stream: Union[BytesIO, StringIO]):


    def clear_results(self):
        self.results.clear()

    def update_results(self):
        submissions = self.get_submissions()
        for submission in submissions:
            if submission in self.results:
                continue
            self.results[submission] = self.evaluator(submission)

    def get_best_result(self) -> Tuple[Path, Tuple[Metric]]:
        return max([(path, result) for path, result in self.results.items()], key=lambda x: x[1])


class SubmissionManager:
    def __init__(self, submissions_dir: Path):
        self.submissions_dir = submissions_dir

    def _create_submissions_dir(self):
        self.submissions_dir.mkdir(parents=True, exist_ok=True)

    def add_participant(self):