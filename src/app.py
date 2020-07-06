import sys, pathlib
import streamlit as st

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from src.login import Login
from src.username_password_manager import UsernamePasswordManager
from src.submissions_manager import SubmissionManager
from src.config import SUBMISSIONS_DIR
from src.submission_sidebar import SubmissionSidebar

@st.cache(allow_output_mutation=True)
def get_login() -> Login:
    password_manager = UsernamePasswordManager()
    return Login(password_manager)

@st.cache(allow_output_mutation=True)
def get_submission_sidebar(username: str, submissions_dir: pathlib.Path) -> SubmissionSidebar:
    submission_manager = SubmissionManager(submissions_dir)
    return SubmissionSidebar(username, submission_manager)


login = get_login()
login.init()

if login.run_and_return_if_access_is_allowed():
    if not login.has_user_signed_out():
        submission_sidebar = get_submission_sidebar(login.get_username(), SUBMISSIONS_DIR)
        submission_sidebar.run()
