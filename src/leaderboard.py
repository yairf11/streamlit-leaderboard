import streamlit as st
import pandas as pd

from src.evaluator import Metric, Evaluator
from src.submissions_manager import SubmissionManager


class Leaderboard:
    def __init__(self, submissions_manager: SubmissionManager,
                 evaluator: Evaluator):
        self.submissions_manager = submissions_manager
        self.evaluator = evaluator

    def display_leaderboard(self):
        participants = self.submissions_manager.participants
        metric_names = [metric.name() for metric in self.evaluator.metrics]
        leaderboard = pd.DataFrame([[pname, *p.get_best_result()[1]] for pname, p in participants.items()],
                                   columns=['Participant Name', *metric_names])
        leaderboard.sort_values(by=metric_names, inplace=True)
        st.table(leaderboard)
