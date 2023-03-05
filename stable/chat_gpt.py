from behaviors import Personality

import re

import openai
openai.api_key = "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"

def chatGPT(user_message: str, personality: Personality, previous_messages = []) -> str:
    start_messages = [
        {
            "role": "system",
            "content": personality.behaviour
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

    text_without_link = re.sub(r'\(.*?\)|https?://\S+', '', message)

    return text_without_link

def get_image(message: str) -> str:
    response = openai.Image.create(
        prompt=message + ". Using modern technologies of photo illustration and have maximum details in the backround and foreground.",
        n=1,
        size="256x256"
    )

    image_url = response['data'][0]['url'] # type: ignore
    return image_url

    
