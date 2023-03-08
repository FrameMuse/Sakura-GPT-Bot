import json
from pathlib import Path

from behaviors import Personality, Personalities

class User:
    def __init__(self, id: int):
        self.id = id
        # Default user data
        self.first_name: "str | None" = None
        self.last_name:  "str | None" = None
        self.user_name:  "str | None" = None

        self.balance:     int = 500 # Balance in Tokens
        # Storage path
        self._storage_file_path = 

    @staticmethod
    def _asd(id: int):
        return Path(f"user-data/{id}/settings.json")

    @staticmethod
    def find(id: int) -> "User | None":

        
        if 
            return None

        return user

    @staticmethod
    def find_all() -> "list[User]":

