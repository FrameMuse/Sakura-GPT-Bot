import openai
import urllib.request
import time

openai.api_key = "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"

def chatGPT(user_message, behaviour, previous_messages=[]):
    start_messages = [
        {
            "role": "system",
            "content": behaviour
        }
    ]
    user_messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    # print(previous_messages)

    messages =  start_messages + previous_messages + user_messages

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )

    return completion.choices[0]["message"]["content"]

def get_image(message:str):
    response = openai.Image.create(
        prompt=message + ". It should be 3D, using modern technologies of photo illustration and have maximum details in the backround and foreground.",
        n=1,
        size="256x256"
    )

    image_url = response['data'][0]['url']

    # image_name = str(time.time())+"-image.png"

    # urllib.request.urlretrieve(image_url, "./images/" + image_name)
    
    return image_url

    
