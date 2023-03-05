import speech_recognition as sr

from pydub import AudioSegment
from gtts import gTTS

import os
import time

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
    return str(text)