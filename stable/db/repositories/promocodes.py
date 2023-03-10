from db.repositories.repository import Repository

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

    def add(self, code: str, tokens: int, expired_at: str = "") -> None:
        self._add_row({
            "code": code,
            "tokens": tokens,
            "created_at": self._timestamp(),
        })

    def find(self, code: str):
        return self._find_by_column("code", code)

# repository = PromocodesRepository()

# repository.add("HARU500",500)

# repository.close()