from pathlib import Path
from typing import List, Callable


class SingleParticipantSubmissions:
    def __init__(self, participant_submission_dir: Path, evaluator: Callable[[Path], float]):
        self.participant_submission_dir = participant_submission_dir
        self.participant_name = self.participant_submission_dir.parts[-1]
        self.evaluator = evaluator

    def get_submissions(self) -> List[Path]:
        return [x for x in self.participant_submission_dir.iterdir() if x.is_file()]

    def


class SubmissionManager:
    def __init__(self, submissions_dir: Path):
        self.submissions_dir = submissions_dir

    def _create_dir(self):
        self.submissions_dir.mkdir(parents=True, exist_ok=True)

    def add_