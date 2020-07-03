from pathlib import Path

import streamlit as st

from src.submissions_manager import SubmissionManager


class SubmissionSidebar:
    def __init__(self, submission_manager: SubmissionManager):
        self.submission_manager = submission_manager

    def run(self):
        st.sidebar.title("Submit Your Results!")

    # def
