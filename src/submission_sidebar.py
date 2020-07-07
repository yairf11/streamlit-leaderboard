from io import BytesIO, StringIO
from pathlib import Path
from typing import Union, Optional

import streamlit as st

from src.submissions_manager import SubmissionManager, SingleParticipantSubmissions


class SubmissionSidebar:
    def __init__(self, username: str, submission_manager: SubmissionManager,
                 submission_file_extension: Optional[str] = None):
        self.username = username
        self.submission_manager = submission_manager
        self.submission_file_extension = submission_file_extension
        self.participant : SingleParticipantSubmissions = None

    def init_participant(self):
        self.submission_manager.add_participant(self.username, exists_ok=True)
        self.participant = self.submission_manager.get_participant(self.username)

    def run(self):
        st.sidebar.title(f"Hello {self.username}!")
        st.sidebar.markdown("## Submit Your Results :fire:")
        self.submit()

    def submit(self):
        submission_io_stream = st.sidebar.file_uploader("Upload your submission file",
                                                        type=self.submission_file_extension)
        submission_name = st.sidebar.text_input('Submission name (optional):', value='', max_chars=30)
        if st.sidebar.button('Submit'):
            if submission_io_stream is None:
                st.sidebar.error('Please upload a submission file.')
            else:
                self._upload_submission(submission_io_stream, submission_name)

    def _upload_submission(self, io_stream: Union[BytesIO, StringIO], submission_name: Optional[str] = None):
        self.init_participant()
        self.participant.add_submission(io_stream, submission_name, self.submission_file_extension)
