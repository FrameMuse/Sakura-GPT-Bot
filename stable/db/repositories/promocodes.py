from db.repositories.repository import Repository
import datetime
from enum import Enum

class PromocodesRepository(Repository):
    def __init__(self):
        super().__init__(
            "promocodes",
            {
                "id": "INTEGER PRIMARY KEY",
                "code": "TEXT",
                "tokens": "INTEGER",
                "expired_at":"TIMESTAMP",
                "created_at": "TIMESTAMP",
            }
        )

    def add(self, code:str, tokens:int,expired_at:str="") -> None:
        self.add_row({
            "code": code,
            "tokens": tokens,
            "created_at": self.timestamp(),
        })

    def find(self,code:str):
        return self.find_by_column("code", code)

# repository = PromocodesRepository()

# repository.add("HARU500",500)

# repository.close()