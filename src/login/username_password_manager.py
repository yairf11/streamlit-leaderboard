from pathlib import Path
from typing import Set, Dict
import json
import argon2


class UsernamePasswordManagerArgon2:
    def __init__(self, passwords_filepath: Path, **argon2_kwargs):
        self.passwords_filepath = passwords_filepath
        self.argon2_hasher = argon2.PasswordHasher(**argon2_kwargs)
        self.user2hash = self._load_user2hash()

    def _load_user2hash(self) -> Dict[str, str]:
        if not self.passwords_filepath.exists():
            return {}
        with self.passwords_filepath.open('r') as f:
            return json.load(f)

    def _dump_user2hash(self):
        with self.passwords_filepath.open('w') as f:
            json.dump(self.user2hash, f)

    def store(self, username: str, password: str):
        self.user2hash[username] = self.argon2_hasher.hash(password)
        self._dump_user2hash()

    def verify(self, username: str, password: str) -> bool:
        try:
            return self.argon2_hasher.verify(self.user2hash[username], password)
        except:
            return False

    def get_all_usernames(self) -> Set[str]:
        return set(self.user2hash.keys())

    def is_username_taken(self, username) -> bool:
        return username in self.user2hash
