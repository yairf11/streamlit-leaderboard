import shutil
from datetime import datetime
from io import BytesIO, StringIO
from pathlib import Path
from typing import List, Callable, Tuple, Dict, Union, Optional

from src.evaluator import Metric, Evaluator
from src.utils import remove_illegal_filename_characters


class SingleParticipantSubmissions:
    def __init__(self, participant_submission_dir: Path, ):
        self.participant_submission_dir = participant_submission_dir
        self._create_participant_dir()
        self.participant_name = self.participant_submission_dir.parts[-1]
        self.results: Dict[Path: Tuple[Metric, ...]] = dict()

    def _create_participant_dir(self):
        self.participant_submission_dir.mkdir(parents=True, exist_ok=True)

    def get_submissions(self) -> List[Path]:
        return [x for x in self.participant_submission_dir.iterdir() if x.is_file()]

    def _add_timestamp_to_string(self, input_string: str) -> str:
        return input_string + '_' + datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%f')

    def _get_submission_name_from_filename(self, filename: str) -> str:
        return ''.join(filename.split('_')[:-1])

    def add_submission(self, io_stream: Union[BytesIO, StringIO], submission_name: Optional[str] = None,
                       file_type_extension: Optional[str] = None):
        submission_name = self._add_timestamp_to_string(submission_name or '')
        file_type_extension = f'.{file_type_extension}' if file_type_extension else ''
        submission_filename = remove_illegal_filename_characters(submission_name) + file_type_extension
        submission_path = self.participant_submission_dir.joinpath(submission_filename)
        with submission_path.open('w') as f:
            io_stream.seek(0)
            shutil.copyfileobj(io_stream, f)

    def clear_results(self):
        self.results.clear()

    def update_results(self, evaluator: Evaluator):
        submissions = self.get_submissions()
        for submission in submissions:
            if submission in self.results:
                continue
            self.results[submission] = evaluator.evaluate(submission)

    def get_best_result(self) -> Tuple[Path, Tuple[Metric, ...]]:
        print(self.participant_name, self.participant_submission_dir)
        return max([(path, result) for path, result in self.results.items()], key=lambda x: x[1])


class SubmissionManager:
    def __init__(self, submissions_dir: Path):
        self.submissions_dir = submissions_dir
        self._create_submissions_dir()
        self._participants = self.load_participant_name2obj()

    @property
    def participants(self) -> Dict[str, SingleParticipantSubmissions]:
        self._update_participants()
        return self._participants

    def _create_submissions_dir(self):
        self.submissions_dir.mkdir(parents=True, exist_ok=True)

    def get_participant(self, participant_name: str) -> SingleParticipantSubmissions:
        return self._participants[participant_name]

    def load_participant_name2obj(self) -> Dict[str, SingleParticipantSubmissions]:
        return {x.parts[-1]: SingleParticipantSubmissions(x) for x in self.submissions_dir.iterdir() if x.is_dir()}

    def _update_participants(self):
        existing_participants = {x.parts[-1] for x in self.submissions_dir.iterdir() if x.is_dir()}
        for participant in self._participants:
            if participant not in existing_participants:
                del self._participants[participant]

    def add_participant(self, participant_name, exists_ok: bool = False):
        participant_name = remove_illegal_filename_characters(participant_name)
        if participant_name in self._participants:
            if not exists_ok:
                raise ValueError(f"Participant {participant_name} already exists!")
            return
        self._participants[participant_name] = SingleParticipantSubmissions(
            self.submissions_dir.joinpath(participant_name))


