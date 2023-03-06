import json
from pathlib import Path

from behaviors import Personality, Personalities


class ChatUser:
    user_id: int
    user_name: str
    user_storage_path: Path

    messages_file_path: Path
    settings_file_path: Path

    messages: "list[dict[str, str]]"
    personality: Personality
    #Monetization part
    tokens: int
    

    def __init__(self, user_name: str , user_id: int):
        self.user_id = user_id
        self.user_storage_path = Path("user-data/" + str(user_id))
        self.user_name = user_name
        self.user_storage_path.parent.mkdir(exist_ok=True, parents=True)

        self.messages = []
        self.messages_file_path = Path(
            self.user_storage_path.as_posix() + "/messages.json")
        self.messages_file_path.parent.mkdir(exist_ok=True, parents=True)

        self.settings_file_path = Path(
            self.user_storage_path.as_posix() + "/settings.json")
        self.settings_file_path.parent.mkdir(exist_ok=True, parents=True)

        # Default personality.
        self.personality = Personalities.Sakura()
        # Default tokens.
        self.tokens = 1000

    def restore_message_history(self):
        """
        Restores previous message history and saves it in `messages` field.

        Unique for each user.
        """

        if not self.messages_file_path.exists():
            return

        file_content = self.messages_file_path.read_text("utf-8")
        file_content_json: list = json.loads(file_content)

        self.messages = file_content_json  # type: ignore

    def restore_settings(self):
        """
        Restores user settings like `tokens`, `personality` and saves them in `settings` field.

        Unique for each user.
        """

        if not self.settings_file_path.exists():
            return

        try:
            file_content = self.settings_file_path.read_text("utf-8")
            file_content_json: dict = json.loads(file_content)

            self.personality = Personalities.find_by_title(file_content_json["personality"])
            self.tokens = file_content_json["tokens"]
            self.user_name = file_content_json["user_name"]
        except:
            # Force set of defaults.
            self.save()
            pass

    def add_message(self, role: str, content: str):
        """
        #param role - "assistant" | "user"

        Adds a new message to `messages` but not saving on disk.

        Use `save` method to save on disk.
        """

        self.messages.append({ "role":role, "content":content })

    def remove_last_message(self):
        self.messages.pop()

    def clear_message_history(self):
        self.messages = []

    def save(self):
        """Saves user data on disk."""

        serialized_messages = json.dumps(self.messages[-6:],ensure_ascii=False,indent=2)
        self.messages_file_path.write_text(serialized_messages, "utf-8")
        
        settings = {
            "personality":self.personality.title,
            "tokens":self.tokens,
            "user_name":self.user_name
        }

        serialized_settings = json.dumps(settings,ensure_ascii=False,indent=2)
        self.settings_file_path.write_text(serialized_settings, "utf-8")
