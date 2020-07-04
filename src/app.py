import sys, pathlib
import streamlit as st

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from src.login import Login
from src.username_password_manager import UsernamePasswordManager
from src.submissions_manager import SubmissionManager
from src.config import SUBMISSIONS_DIR
from src.submission_sidebar import SubmissionSidebar


submission_manager = SubmissionManager(SUBMISSIONS_DIR)
password_manager = UsernamePasswordManager()

login = Login(password_manager, submission_manager)
if login.run_and_return_if_access_is_allowed():
    submissions_sidebar = SubmissionSidebar(SubmissionManager(SUBMISSIONS_DIR))
    submissions_sidebar.run()



