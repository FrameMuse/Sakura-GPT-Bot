import os
from pathlib import Path

from tokens import Tokens
from serializable import Serializable


USER_DATA_DIRECTORY = "/root/anus/stable/user-data"

class User(Serializable):
    def __init__(self, id: int):
        # Fields to serialize
        super().__init__({
            "first_name": str,
            "last_name": str,
            "user_name": str,
            "balance": Tokens
        })
        
        self.id = id
        # Default user data
        self.first_name: "str | None" = None
        self.last_name:  "str | None" = None
        self.user_name:  "str | None" = None
        self.balance: Tokens = Tokens(500)
        # Storage path
        self.__storage_file_path = User.__get_storage_path(id)
        self.__storage_file_path.parent.mkdir(exist_ok=True, parents=True)

        self.__initiate()
        self.__initiated = True
        self.__handle_updates()

    def __initiate(self):
        """
        Serialize and deserialize sequence.
        """

        if self.__storage_file_path.exists():
            # Deserialize existing data.
            self._assign_fromJSON(self.__storage_file_path.read_text())
        else:
            self.__serialize()

    def __serialize(self):
        """
        Serialize current object and write in `settings.json`
        """

        self.__storage_file_path.write_text(self._toJSON())

    def __handle_updates(self):
        # Serialize balance on amount update.
        self.balance.on_amount_update(lambda: self.__serialize())

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        
        if "_User__initiated" not in self.__dict__: return
        if key not in self._fields: return

        self.__serialize()

    @staticmethod
    def __get_storage_path(id: int):
        return Path(f"{USER_DATA_DIRECTORY}/{id}/user.json")

    @staticmethod
    def findall() -> "list[User]":
        users: "list[User]" = []
        for user_id in os.listdir(USER_DATA_DIRECTORY):
            user_id = int(user_id)
            user = User(user_id)
            users.append(user)

        return users
