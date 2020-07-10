import sys, pathlib

import streamlit as st

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from src.login import Login
from src.username_password_manager import UsernamePasswordManager
from src.submissions_manager import SubmissionManager
from src.config import SUBMISSIONS_DIR, EVALUATOR_CLASS, EVALUATOR_KWARGS
from src.submission_sidebar import SubmissionSidebar
from src.evaluator import Evaluator
from src.leaderboard import Leaderboard

@st.cache(allow_output_mutation=True)
def get_login() -> Login:
    password_manager = UsernamePasswordManager()
    return Login(password_manager)

@st.cache(allow_output_mutation=True)
def get_submission_manager():
    return SubmissionManager(SUBMISSIONS_DIR)

@st.cache(allow_output_mutation=True)
def get_submission_sidebar(username: str) -> SubmissionSidebar:
    return SubmissionSidebar(username, get_submission_manager(),
                             submission_validator=get_evaluator().validate_submission)

@st.cache(allow_output_mutation=True)
def get_evaluator() -> Evaluator:
    return EVALUATOR_CLASS(**EVALUATOR_KWARGS)

@st.cache(allow_output_mutation=True)
def get_leaderboard() -> Leaderboard:
    return Leaderboard(get_submission_manager(), get_evaluator())


login = get_login()
login.init()

if login.run_and_return_if_access_is_allowed():
    if not login.has_user_signed_out():
        get_submission_sidebar(login.get_username()).run()
        get_leaderboard().display_leaderboard()

