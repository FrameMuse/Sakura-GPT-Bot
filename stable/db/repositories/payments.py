from repository import Repository

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

    def set_status(self, payment_id: str, status: Status):
        self._update_column("payment_id", payment_id, "status", status.name)
        self._update_column("payment_id", payment_id, "updated_at", self._timestamp())

repository = PaymentsRepository()
repository.create("SUKA:20012299",12303,300)
repository.create("SUKA:2001992111213",12303,300)
repository.set_status("SUKA:200199",repository.Status.SUCCEEDED)