import time

import openai
import telebot
from telebot import types

import re

from behaviors import Behaviors

from chat_user import ChatUser
from chat_gpt import chatGPT
from chat_gpt import get_image
from voice import collect_garbage, ogg_to_wav, recognize, text_to_speech

from dotenv import load_dotenv
import os

import discord
from discord.ext import commands

load_dotenv()
openai.api_key = os.environ.get("OPEN_AI_KEY")

white_list = ["akaipureya","framemuse","kukushka","fckuloony"]
channel_list = [883733235471892510,1081318059781914735]

discord_intents = discord.Intents.all()
discord_intents.members = True
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
token = os.environ.get("DISCORD_KEY")
client = commands.Bot(command_prefix='',intents=discord_intents)

@client.event
async def on_ready():
    print('Bot Is Ready!')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith("!q"):
        return
    if message.content.startswith("!c"):
        chat_user = ChatUser(message.channel.id)
        chat_user.clear_message_history()
        chat_user.save()
        return
    # print(type(message.channel.id))
    if message.channel.id not in channel_list or message.author.name.lower() not in white_list :
        return

    chat_user = ChatUser(message.channel.id)
    chat_user.restore_message_history()


    chat_gpt_response = chatGPT(message.content, chat_user.behaviour, chat_user.messages)
    chat_gpt_response_chunks = []
    chat_gpt_response_chunks.append(chat_gpt_response[0:2000])
    if len(chat_gpt_response) > 2000:
        chat_gpt_response_chunks.append(chat_gpt_response[2000:-1])

    channel = client.get_channel(message.channel.id)
    if not channel:
        raise ValueError("Channel not found.")
    for response_chunk in chat_gpt_response_chunks:
        await channel.send(response_chunk)
        


    chat_user.add_message("user", message.content)
    chat_user.add_message("assistant", chat_gpt_response)
    chat_user.save()

@client.event
async def on_raw_reaction_add(event):
    channel = await client.fetch_channel(event.channel_id)

    chat_user = ChatUser(event.channel_id)
    chat_user.restore_message_history()
    
    
    chat_gpt_response = chatGPT("My reaction on your answer is " + str(event.emoji), chat_user.behaviour, chat_user.messages)

    await channel.send(chat_gpt_response)

client.run(str(token))

# bot = telebot.TeleBot(str(token))

# last_message = []

# regex = r"\[image description: (.*?)]"

# @bot.message_handler(commands=["start"])
# def start_command(message):

#     behaviors_list = Behaviors.get_names()
    
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
#     buttons = [types.KeyboardButton(name) for name in behaviors_list]
    
#     markup.add(*buttons)

#     bot.send_message(message.chat.id, "Привет, я чат-бот Sakura! Я могу вести с тобой диалог, и понимать контекст сказанного тобой!", reply_markup=markup)


# @bot.message_handler(commands=["image"])
# def image_command(message):
#     response = openai.Image.create(
#         prompt=message.text,
#         n=1,
#         size="1024x1024"
#     )

#     image_url = response['data'][0]['url']

#     bot.send_message(message.chat.id, image_url)


# @bot.message_handler(content_types=["text"])
# def text(message):
#     url = "none"
#     chat_user = ChatUser(message.from_user.id)
#     chat_user.restore_message_history()
#     chat_user.restore_settings()
    

#     behaviors_dict = {}
#     for behavior in Behaviors.__dict__:
#         if not behavior.startswith('__') and behavior != "get_names":
#             behaviors_dict[Behaviors.__dict__[behavior].name] = Behaviors.__dict__[behavior]

#     if message.text in behaviors_dict:
        
#         chat_user.behavior = behaviors_dict[message.text].behaviour
#         bot.send_chat_action(message.chat.id, "typing")
#         chat_user.clear_message_history()
#         message_content = chatGPT("Привет!", chat_user.behavior + " Человека с которым ты общаешься зовут " + message.from_user.first_name , chat_user.messages)
#         result = re.search(r"\[image description: (.*?)\]", message_content)


#         if result:
#             image_description = result.group(1)
#             print(image_description)
#             url = get_image(image_description)
#             message_content = message_content.replace("[image description: " + result.group(1) + "]", "")
#         else:
#             print("No image description found.")
        
#         bot.send_message(message.chat.id, message_content)
        
#         chat_user.save()
#         return

#     bot.send_chat_action(message.chat.id, "typing")
#     message_content = chatGPT(message.text, chat_user.behavior , chat_user.messages)

#     result = re.search(r"\[image description: (.*?)\]", message_content)


#     if result:
#         image_description = result.group(1)
#         print(image_description)
#         url = get_image(image_description)
#         message_content = message_content.replace("[image description: " + result.group(1) + "]", "")
#     else:
#         print("No image description found.")

#     sent_message = bot.send_message(message.chat.id, message_content,)

#     if url != "none":
#         bot.send_photo(message.chat.id,photo=url)

#     last_message.append(sent_message)

#     chat_user.add_message("user",message.text)
#     chat_user.add_message("assistant",message_content)
#     chat_user.save()


# @bot.edited_message_handler(func=lambda message: True)
# def edit_text(message):
#     chat_user = ChatUser(message.from_user.id)
#     chat_user.restore_message_history()

#     bot.send_chat_action(message.chat.id, "typing")
#     message_content = chatGPT(message.text, chat_user.behavior, chat_user.messages)

#     bot.edit_message_text(chat_id=message.chat.id,
#                           message_id=last_message[-1].id, text=message_content)


# @bot.message_handler(content_types=["voice"])
# def voice(message):
#     chat_user = ChatUser(message.from_user.id)
#     chat_user.restore_message_history()
    
#     # display "typing" status bar
#     bot.send_chat_action(message.chat.id, "typing")

#     file_info = bot.get_file(message.voice.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)

#     file_name = str(time.time()) + "-voice.ogg"
#     with open(file_name, "wb") as new_file:
#         new_file.write(downloaded_file)

#     ogg_to_wav(file_name)
#     text = recognize(file_name.replace(".ogg", ".wav"))
#     chat_user.add_message("user",str(text))
    
#     sent_message = bot.send_message(message.chat.id, str(text))

#     bot.send_chat_action(message.chat.id, "typing")

#     message_content = chatGPT(text, chat_user.behavior, chat_user.messages)
#     chat_user.add_message("assistant",message_content)

#     bot.reply_to(sent_message, message_content)

#     bot.send_chat_action(message.chat.id, "record_audio")
#     speech_file_name = text_to_speech(message_content)
#     speech_file = open(speech_file_name, "rb")

#     bot.send_chat_action(message.chat.id, "upload_audio")
#     bot.send_voice(message.chat.id, speech_file,
#                    reply_to_message_id=sent_message.id)

#     chat_user.save()
#     collect_garbage([file_name, file_name.replace(
#         ".ogg", ".wav"), speech_file_name])





# bot.infinity_polling()
