import sys, pathlib

import streamlit as st

from src.common.css_utils import set_block_container_width

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from src.login.login import Login
from src.login.username_password_manager import UsernamePasswordManagerArgon2
from src.submissions.submissions_manager import SubmissionManager
from src.config import SUBMISSIONS_DIR, EVALUATOR_CLASS, EVALUATOR_KWARGS, PASSWORDS_FILE, ARGON2_KWARGS, \
    ALLOWED_SUBMISSION_FILE_EXTENSION
from src.submissions.submission_sidebar import SubmissionSidebar
from src.evaluation.evaluator import Evaluator
from src.display.leaderboard import Leaderboard
from src.display.personal_progress import PersonalProgress


@st.cache(allow_output_mutation=True)
def get_login() -> Login:
    password_manager = UsernamePasswordManagerArgon2(PASSWORDS_FILE, **ARGON2_KWARGS)
    return Login(password_manager)


@st.cache(allow_output_mutation=True)
def get_submission_manager():
    return SubmissionManager(SUBMISSIONS_DIR)


@st.cache(allow_output_mutation=True)
def get_submission_sidebar(username: str) -> SubmissionSidebar:
    return SubmissionSidebar(username, get_submission_manager(),
                             submission_validator=get_evaluator().validate_submission,
                             submission_file_extension=ALLOWED_SUBMISSION_FILE_EXTENSION)


@st.cache(allow_output_mutation=True)
def get_evaluator() -> Evaluator:
    return EVALUATOR_CLASS(**EVALUATOR_KWARGS)


@st.cache(allow_output_mutation=True)
def get_leaderboard() -> Leaderboard:
    return Leaderboard(get_submission_manager(), get_evaluator())


@st.cache(allow_output_mutation=True)
def get_personal_progress(username: str) -> PersonalProgress:
    return PersonalProgress(get_submission_manager().get_participant(username), get_evaluator())


login = get_login()
login.init()
leaderboard_placeholders = st.empty()
progress_placeholder = st.empty()

if login.run_and_return_if_access_is_allowed():
    if not login.has_user_signed_out():
        get_submission_sidebar(login.get_username()).run_submission()
        get_leaderboard().display_leaderboard(leaderboard_placeholders)
        if get_submission_manager().participant_exists(login.get_username()):
            get_personal_progress(login.get_username()).show_progress(progress_placeholder)

        max_width_value = st.sidebar.slider("Select max-width in px", 100, 2000, 1200, 100)
        set_block_container_width(max_width_value)
