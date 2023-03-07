from restricted_words import RestrictedWords
from behaviors import Personality, Apology

import re

import openai
openai.api_key = "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"

def chatGPT(user_message: str, personality: Personality, previous_messages = []) -> str:
    if RestrictedWords.presence(user_message):
        return personality.apologize_for(Apology.UsageOfRestrictedWords)
    
    start_messages = [
        {
            "role": "system",
            "content": personality.behaviour + ". Avoid using swears in russian language in any sentence."
        }
    ]
    user_messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    messages = start_messages + previous_messages + user_messages

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        temperature=personality.temperature
    )

    message = completion.choices[0]["message"]["content"] # type: ignore
    message_filtered = RestrictedWords.replace(message, "")

    text_without_link = re.sub(r'\(.*?\)|https?://\S+', '', message_filtered)
    return text_without_link

def get_image(prompt: str):
    if RestrictedWords.presence(prompt):
        return

    response = openai.Image.create(
        prompt=prompt + ". Using modern technologies of photo illustration and have maximum details in the backround and foreground.",
        n=1,
        size="256x256"
    )

    image_url: str = response['data'][0]['url'] # type: ignore
    return image_url
