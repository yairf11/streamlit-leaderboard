from pathlib import Path

import streamlit as st

from src.submissions_manager import SubmissionManager


class SubmissionSidebar:
    def __init__(self, username: str, submission_manager: SubmissionManager):
        self.username = username
        self.submission_manager = submission_manager

    def run(self):
        st.sidebar.title(f"Hello {self.username}!")
        st.sidebar.markdown("## Submit Your Results :fire:")

    # def
