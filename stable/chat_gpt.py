from restricted_words import RestrictedWords
from personalities import Personality, Apology
from db.repositories.openai_usage import OpenAIUsageRepository

from dotenv import load_dotenv
import os

import openai

load_dotenv()

openai.api_key = os.environ.get("OPEN_AI_KEY")

RESPONSE_TOKENS_LIMIT = 2400

def chatGPT(prompt: str, personality: Personality, previous_messages = []) -> str:
    # Restrict using some words.
    if RestrictedWords.presence(prompt):
        return personality.apologize_for(Apology.UsageOfRestrictedWords)
    
    # Gather messages.
    start_messages = [
        {
            "role": "system",
            "content": personality.behaviour + ". Avoid using swears in russian language in any sentence."
        }
    ]
    user_messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    messages = start_messages + previous_messages + user_messages

    # Request to openai.
    model = "gpt-3.5-turbo"
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=personality.temperature,
        max_tokens=RESPONSE_TOKENS_LIMIT,
        top_p=1
    )
    message = completion.choices[0]["message"]["content"] # type: ignore

    # Save information about usage.
    repository = OpenAIUsageRepository()
    repository.add(repository.Type.TEXT, model, prompt, message)
    repository.close()

    # Process the message.
    message_filtered = RestrictedWords.replace(message)
    return message_filtered
