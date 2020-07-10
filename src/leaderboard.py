from typing import Dict

import streamlit as st
import pandas as pd

from src.evaluator import Evaluator
from src.submissions_manager import SubmissionManager, SingleParticipantSubmissions


class Leaderboard:
    def __init__(self, submissions_manager: SubmissionManager,
                 evaluator: Evaluator):
        self.submissions_manager = submissions_manager
        self.evaluator = evaluator

    @st.cache(hash_funcs={SingleParticipantSubmissions: lambda x: x.submissions_hash()})
    def _get_sorted_leaderboard(self, participants_dict: Dict[str, SingleParticipantSubmissions]) -> pd.DataFrame:
        print('ran again!')
        for participant in participants_dict.values():
            participant.update_results(self.evaluator)
        metric_names = [metric.name() for metric in self.evaluator.metrics()]
        leaderboard = pd.DataFrame([[pname, *best_result[1]] for pname, best_result in
                                     [(pname, p.get_best_result()) for pname, p in participants_dict.items()]
                                     if best_result is not None],
                                   columns=['Participant Name', *metric_names])
        leaderboard = leaderboard.sort_values(by=metric_names, ascending=False, ignore_index=True)
        leaderboard.index += 1
        return leaderboard


    def display_leaderboard(self):
        leaderboard = self._get_sorted_leaderboard(self.submissions_manager.participants)
        st.table(leaderboard)
