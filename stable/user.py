import telebot

import os
from dotenv import load_dotenv
from pathlib import Path

from tokens import Tokens
from promocodes import Promocodes
from daily import DailyTokens
from personalities import Personality, Personalities
from messages_history import MessageHistory

from serializable import Serializable

load_dotenv()

USER_DATA_DIRECTORY = os.environ.get("USER_DATA_DIRECTORY")

class User(Serializable):
    def __init__(self, id: int):
        # Fields to serialize
        super().__init__({
            "first_name":      str,
            "last_name":       str,
            "username":        str,
            "balance":         Tokens,
            "promocodes":      Promocodes,
            "daily_tokens":    DailyTokens,
            "personality":     Personalities.find_by_title,
            "message_history": MessageHistory,
        })
        
        self.id = id
        # Default user data
        self.first_name: str = ""
        self.last_name:  str = ""
        self.username:   str = ""
        #
        self.balance:         Tokens         = Tokens()
        self.promocodes:      Promocodes     = Promocodes()
        self.daily_tokens:    DailyTokens    = DailyTokens()
        self.personality:     Personality    = Personalities.Sakura()
        self.message_history: MessageHistory = MessageHistory()
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
        # Credit tokens to balance.
        self.promocodes.on_applied(lambda tokens: self.balance.credit(tokens))
        # Credit tokens to balance.
        self.daily_tokens.on_obtain(lambda tokens: self.balance.credit(tokens))
        # Serialize messages history on its update.
        self.message_history.on_updated(lambda: self.__serialize())

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

    @staticmethod
    def from_telebot(from_user: telebot.types.User) -> "User":
        """
        Retrieves from `telebot.types.User`.
        """

        user = User(from_user.id)
        user.first_name = from_user.first_name
        user.last_name  = from_user.last_name
        user.username   = from_user.username

        return user


# user = User(-101)
# # print(user.message_history)
# user.message_history.add(MessageHistory.Role.ASSISTANT, "Penis")
# user.message_history.add(MessageHistory.Role.USER, "Jopa")
# print(user.message_history)
# user.message_history.remove_last()
# print(user.message_history.get(2))
