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

        # placeholders
        self.first_login_checkbox_placeholder = st.sidebar.empty()
        self.username_placeholder = st.sidebar.empty()
        self.pwd_placeholder = st.sidebar.empty()
        self.pwd2_placeholder = st.sidebar.empty()

    def get_username(self) -> str:
        return self.session_state.username

    def clear_placeholders(self):
        self.first_login_checkbox_placeholder.empty()
        self.username_placeholder.empty()
        self.pwd_placeholder.empty()
        self.pwd2_placeholder.empty()

    def run_and_return_if_access_is_allowed(self) -> bool:
        if (not self.password_manager.is_username_taken(self.session_state.username)) or \
                (not self.session_state.is_logged_in):
            self.session_state.is_logged_in = False
            is_first_login = self.first_login_checkbox_placeholder.checkbox("This is my first login", value=False)
            if is_first_login:
                is_logged_in = self.try_signup()
            else:
                is_logged_in = self.try_login()
            if is_logged_in:
                self.clear_placeholders()
        return True

    def try_login(self) -> bool:
        username = self.username_placeholder.text_input("Username:", value="", max_chars=30)
        pwd = self.pwd_placeholder.text_input("Password:", value="", type="password", max_chars=30)
        self.session_state.username = username
        if (self.password_manager.is_username_taken(self.session_state.username)) and \
                (pwd == self.password_manager.decrypt(self.session_state.username)):
            self.session_state.is_logged_in = True
            return True
        else:
            st.error("The username or password you entered is incorrect")
            return False

    def _is_valid_username(self, username: str) -> bool:
        return (len(username) > 0) and remove_illegal_filename_characters(username) == username

    def try_signup(self) -> bool:
        username = self.username_placeholder.text_input("Username:", value="", max_chars=30)
        pwd = self.pwd_placeholder.text_input("Password:", value="", type="password", max_chars=30)
        pwd2 = self.pwd2_placeholder.text_input("Retype password:", value="", type="password", max_chars=30)

        if not self._is_valid_username(username):
            st.sidebar.error('Invalid username. Must have only alphanumeric or ".-_ " characters, '
                     'without trailing or leading whitespaces.')
        elif self.password_manager.is_username_taken(username):
            st.sidebar.error("Username already exists.")
        elif pwd != pwd2:
            st.sidebar.error('Passwords do not match.')
        elif len(pwd) == 0:
            st.sidebar.error('Please choose a password')
        else:
            self.session_state.username = username
            self.password_manager.encrypt(username, pwd)
            self.session_state.is_logged_in = True
            return True
        return False
