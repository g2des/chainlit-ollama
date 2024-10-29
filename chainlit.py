"""Chainlit app interface."""
from typing import List, LiteralString

import chainlit as cl
import chainlit.logger as logger
from ollama import Options


from chainlit_ollama import utils as clutils
from chainlit_ollama import ollama as ollmutils 
from chainlit_ollama.messages import on_messages
import chainlit_ollama.settings as clsettings

async def get_models() -> List[LiteralString]:
    return  ollmutils.get_models()


@cl.set_chat_profiles
async def chat_profile(current_user: cl.User)-> List:
    return clutils.chat_profiles

@cl.on_chat_start
async def start_chat():
    await clutils.start_chat()


@cl.on_settings_update
async def settings_update(settings):
    clsettings.settings(settings=settings)
    

@cl.on_message
async def message(message: cl.Message):
    await on_messages(message=message)
