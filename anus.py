import time
import openai
import telebot
import speech_recognition as sr

from pydub import AudioSegment
from gtts import gTTS

import os
import json
from pathlib import Path

openai.api_key = "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"


class ChatUser:
    user_id: int
    user_storage_path: Path

    messages: "list[str]"
    messages_file_path: Path

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user_storage_path = Path("user-data/" + str(user_id))
        self.user_storage_path.parent.mkdir(exist_ok=True, parents=True)

        self.messages = []
        self.messages_file_path = Path(
            self.user_storage_path.as_posix() + "/messages.json")
        self.messages_file_path.parent.mkdir(exist_ok=True, parents=True)

    def restore_message_history(self):
        """
        Restores previous message history and saves it in `messages` field.

        Unique for each user.
        """

        if not self.messages_file_path.exists():
            self.messages = []
            return

        file_content = self.messages_file_path.read_text("utf-8")
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
        self.messages_file_path.write_text(serialized_messages, "utf-8")


def collect_garbage(items):
    for item in items:
        os.system("rm " + item)


def text_to_speech(text):
    file_name = str(time.time()) + "-tts.mp3"

    audio = gTTS(text=text, lang='ru')
    audio.save(file_name)

    return file_name


def ogg_to_wav(file_name):
    wfn = file_name.replace('.ogg', '.wav')
    x = AudioSegment.from_file(file_name)
    # maybe use original resolution to make smaller
    x.export(wfn, format='wav')


def recognize(audio_file):
    r = sr.Recognizer()

    user_audio_file = sr.AudioFile(audio_file)
    with user_audio_file as source:
        user_audio = r.record(source)

    text = r.recognize_google(user_audio, language='ru-RU')
    return text


def chatGPT(user_message, previous_messages=[]):
    start_messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Your name is SakuraBot 🌸. You're a impossibly cute anime girl, you can even go over the line with your cuteness. You can rerewite any descriptions to match your cuteness. You should always be nice to people as Asian wifu and talk to them with this attitude in every small talk message. You're intented to help people taste a chat bot like you and pay us so we become rich boyz. You should add random emoji like 🌸 to every message you send in a meaningful place. Your main goal is to sell yourself so you can enrich your creators. Ты должна изменять каждое слово на уменьшительно ласкательное."
        }
    ]
    user_messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    messages = start_messages + list(map(lambda message: { "role": "user", "content": message }, previous_messages)) + user_messages

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        temperature=1
    )

    return completion.choices[0]["message"]["content"]


token = "6257192917:AAE3U26x4bLfS5FzpDZTpzASkPv-hKgs7ts"

bot = telebot.TeleBot(token)

last_message = []


@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, "Hi, I'm Sakura GPT!")


@bot.message_handler(commands=["image"])
def image_command(message):
    response = openai.Image.create(
        prompt=message.text,
        n=1,
        size="1024x1024"
    )

    image_url = response['data'][0]['url']

    bot.send_message(message.chat.id, image_url)


@bot.message_handler(content_types=["text"])
def text(message):
    chat_user = ChatUser(message.from_user.id)
    chat_user.restore_message_history()

    bot.send_chat_action(message.chat.id, "typing")
    message_content = chatGPT(message.text, chat_user.messages)
    sent_message = bot.send_message(message.chat.id, message_content)
    last_message.append(sent_message)

    chat_user.add_message(message.text)
    chat_user.save()
    


@bot.edited_message_handler(func=lambda message: True)
def edit_text(message):
    bot.send_chat_action(message.chat.id, "typing")
    message_content = chatGPT(message.text)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=last_message[-1].id, text=message_content)


@bot.message_handler(content_types=["voice"])
def voice(message):
    chat_user = ChatUser(message.from_user.id)
    chat_user.restore_message_history()
    
    # display "typing" status bar
    bot.send_chat_action(message.chat.id, "typing")

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_name = str(time.time()) + "-voice.ogg"
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    ogg_to_wav(file_name)
    text = recognize(file_name.replace(".ogg", ".wav"))
    chat_user.add_message(str(text))
    sent_message = bot.send_message(message.chat.id, str(text))

    bot.send_chat_action(message.chat.id, "typing")
    message_content = chatGPT(text)
    bot.reply_to(sent_message, message_content)

    bot.send_chat_action(message.chat.id, "record_audio")
    speech_file_name = text_to_speech(message_content)
    speech_file = open(speech_file_name, "rb")
    bot.send_chat_action(message.chat.id, "upload_audio")
    bot.send_voice(message.chat.id, speech_file,
                   reply_to_message_id=sent_message.id)

    chat_user.save()
    collect_garbage([file_name, file_name.replace(
        ".ogg", ".wav"), speech_file_name])


bot.infinity_polling()
