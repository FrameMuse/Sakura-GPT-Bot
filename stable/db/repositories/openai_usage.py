from db.repositories.repository import Repository

from enum import Enum

class OpenAIUsageRepository(Repository):
    class Type(Enum):
        TEXT = 0
        IMAGE = 1
    
    def __init__(self):
        super().__init__(
            "openai_usage",
            {
                "id": "INTEGER PRIMARY KEY",
                "type": "TEXT",
                "model": "TEXT",
                "prompt_chars": "INTEGER",
                "response_chars": "INTEGER",
                "created_at": "TIMESTAMP"
            }
        )

    def add(self, type: Type, model: str, prompt: str = "", response: str = "") -> None:
        self.add_row({
            "type": type.name,
            "model": model,
            "prompt_chars": len(prompt),
            "response_chars": len(response),
            "created_at": self.timestamp()
        })

