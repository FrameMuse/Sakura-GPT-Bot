from restricted_words import RestrictedWords
from personalities import Personality, Apology
from db.repositories.openai_usage import OpenAIUsageRepository

import re

from dotenv import load_dotenv
import os

import openai

load_dotenv()

openai.api_key = os.environ.get("OPEN_AI_KEY")

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
    model = "gpt-3.5-turbo-0301"
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=personality.temperature
    )
    message = completion.choices[0]["message"]["content"] # type: ignore

    # Save information about usage.
    repository = OpenAIUsageRepository()
    repository.add(repository.Type.TEXT, model, prompt, message)
    repository.close()

    # Process the message.
    message_filtered = RestrictedWords.replace(message)

    # Remove potenial [image description] in the message.
    text_without_link = re.sub(r'\(.*?\)|https?://\S+', '', message_filtered)
    return text_without_link

def get_image(prompt: str):
    prompt += ". Using modern technologies of photo illustration and have maximum details in the backround and foreground."
    
    if RestrictedWords.presence(prompt):
        return
    
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )

     # Save information about usage.
    repository = OpenAIUsageRepository()
    repository.add(repository.Type.IMAGE, "dall-e")
    repository.close()

    image_url: str = response['data'][0]['url'] # type: ignore
    return image_url
