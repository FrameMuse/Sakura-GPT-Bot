import json
from enum import Enum
from pyee.twisted import TwistedEventEmitter
from serializable import Serializable

DEFAULT_MESSAGES_SLICE = 6 # 3 Context messages

class MessageHistory(Serializable):
    class Role(Enum):
        USER = "user"
        ASSISTANT = "assistant"
    
    def __init__(self, __list: "list[dict[str, str]] | str" = []):
        if isinstance(__list, list):
            self.__list = __list
        if isinstance(__list, str):
            self.__list = json.loads(__list)
        
        self.__events = TwistedEventEmitter()

    # def represents(self):
    #     return self.__list

    def __str__(self) -> str:
        return json.dumps(self.__list, indent=4, ensure_ascii=False)
    
    def add(self, role: Role, content: str):
        """
        #param role - "assistant" | "user"

        Adds a new message to `messages` but not saving on disk.

        Use `save` method to save on disk.
        """

        self.__list.append({ "role": role.value, "content": content })
        self.__events.emit("updated")

    def get(self, slice: int = DEFAULT_MESSAGES_SLICE) -> "list[dict[str, str]]":
        return self.__list[-slice:]

    def remove_last(self):
        self.__list.pop()
        self.__events.emit("updated")

    def clear(self):
        self.__list = []
        self.__events.emit("updated")

    def on_updated(self, callback):
        self.__events.on("updated", callback)