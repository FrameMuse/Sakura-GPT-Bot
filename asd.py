import json
from pathlib import Path


class ChatUser:
    user_id: int
    user_storage_path: Path

    messages: list
    messages_file_path: Path

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user_storage_path = Path("user-data/" + str(user_id))
        self.user_storage_path.parent.mkdir(exist_ok=True, parents=True)

        self.messages = []
        self.messages_file_path = Path(
            self.user_storage_path.as_posix() + "/messages.json")
        self.messages_file_path.parent.mkdir(exist_ok=True, parents=True)

    def restore(self):
        """
        Restores previous message history and saves it in `messages` field.

        Unique for each user.
        """

        file = open(self.messages_file_path, "r")
        file_content = file.read()
        file_content_json: list = json.loads(file_content)

        self.messages = file_content_json  # type: ignore

    def add_message(self, message: str):
        """
        Adds a new message to `messages` but not saving on disk.

        Use `save` method to save on disk.
        """

        self.messages.append(message)

    def save(self):
        """Saves user data on disk."""

        serialized_messages = json.dumps(self.messages)

        file = open(self.messages_file_path, "w")
        file.write(serialized_messages)
        file.close()
