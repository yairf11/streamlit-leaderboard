from datetime import datetime
import pandas as pd

from src.evaluator import Evaluator
from src.submissions_manager import SingleParticipantSubmissions


class PersonalProgress:
    def __init__(self, participant_submissions: SingleParticipantSubmissions, evaluator: Evaluator,
                 start_time: datetime, end_time: datetime):
        self.participant_submissions = participant_submissions
        self.evaluator = evaluator
        self.start_time = start_time
        self.end_time = end_time

    def show_progress(self):
        self.participant_submissions.update_results(evaluator=self.evaluator)
        metric_names = [metric.name() for metric in self.evaluator.metrics()]



        leaderboard = pd.DataFrame([[pname, *best_result[1]] for pname, best_result in
                                     [(pname, p.get_best_result()) for pname, p in participants_dict.items()]
                                     if best_result is not None],
                                   columns=['Participant Name', *metric_names])
