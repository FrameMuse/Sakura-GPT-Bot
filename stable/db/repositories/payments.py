from db.repositories.repository import Repository

from enum import Enum


class PaymentsRepository(Repository):
    class Status(Enum):
        CREATED = 0
        SUCCEEDED = 1

    def __init__(self):
        super().__init__(
            "payments",
            {
                "id": "INTEGER PRIMARY KEY",
                "payment_id": "TEXT",
                "user_id": "INTEGER",
                "status": "TEXT",
                "tokens": "INTEGER",
                "created_at": "TIMESTAMP",
                "updated_at": "TIMESTAMP"
            }
        )

    def create(self, payment_id: str, user_id: int, tokens: int, status: Status=Status.CREATED) -> None:
        self._add_row({
            "payment_id": payment_id,
            "user_id": user_id,
            "status": status.name,
            "tokens": tokens,
            "created_at": self._timestamp(),
            "updated_at": self._timestamp(),
        })

    def find(self, payment_id: str):
        return self._find_by_column("payment_id", payment_id)

    def set_status(self, payment_id: str, status: Status):
        self._update_column("payment_id", payment_id, "status", status.name)
        self._update_column("payment_id", payment_id, "updated_at", self._timestamp())
