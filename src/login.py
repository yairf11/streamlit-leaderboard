import streamlit as st

from src.session_state import get_session_state
from src.submissions_manager import SubmissionManager
from src.username_password_manager import UsernamePasswordManager
from src.utils import remove_illegal_filename_characters


class Login:
    def __init__(self, password_manager: UsernamePasswordManager, submission_manager: SubmissionManager):
        self.password_manager = password_manager
        self.submission_manager = submission_manager
        self.session_state = get_session_state(username='', is_logged_in=False)

    def get_username(self) -> str:
        return self.session_state.username

    def run_and_return_if_access_is_allowed(self) -> bool:
        if (not self.password_manager.is_username_taken(self.session_state.username)) or \
                (not self.session_state.is_logged_in):
            self.session_state.is_logged_in = False
            is_first_login = st.sidebar.checkbox("This is my first login", value=False)
            if is_first_login:
                return self.try_signup()
            else:
                return self.try_login()
        return True

    def try_login(self) -> bool:
        username_placeholder = st.sidebar.empty()
        pwd_placeholder = st.sidebar.empty()

        username = username_placeholder.text_input("Username:", value="", max_chars=30)
        pwd = pwd_placeholder.text_input("Password:", value="", type="password", max_chars=30)
        self.session_state.username = username
        self.session_state.password = pwd
        if (self.password_manager.is_username_taken(self.session_state.username)) and \
                (self.session_state.password == self.password_manager.decrypt(self.session_state.username)):
            username_placeholder.empty()
            pwd_placeholder.empty()
            self.session_state.is_logged_in = True
            return True
        else:
            st.error("The username or password you entered is incorrect")
            return False

    def _is_valid_username(self, username: str) -> bool:
        return (len(username) > 0) and remove_illegal_filename_characters(username) == username

    def try_signup(self) -> bool:
        username_placeholder = st.sidebar.empty()
        pwd_placeholder = st.sidebar.empty()
        pwd2_placeholder = st.sidebar.empty()

        username = username_placeholder.text_input("Username:", value="", max_chars=30)
        pwd = pwd_placeholder.text_input("Password:", value="", type="password", max_chars=30)
        pwd2 = pwd2_placeholder.text_input("Retype password:", value="", type="password", max_chars=30)

        if not self._is_valid_username(username):
            st.sidebar.error('Invalid username. Must have only alphanumeric or ".-_ " characters, '
                     'without trailing or leading whitespaces.')
            return False

        if self.password_manager.is_username_taken(username):
            st.sidebar.error("Username already exists.")
            return False

        if pwd != pwd2:
            st.error('Passwords do not match.')
            return False

        self.session_state.username = username
        self.session_state.password = pwd
        self.password_manager.encrypt(username, pwd)
        username_placeholder.empty()
        pwd_placeholder.empty()
        pwd2_placeholder.empty()
        self.session_state.is_logged_in = True
        return True

