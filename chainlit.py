"""Chainlit app interface."""
from typing import List, LiteralString

import chainlit as cl
import chainlit.logger as logger
from ollama import Options


from chainlit_ollama import utils as clutils
from chainlit_ollama import ollama as ollmutils 

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
    logger.info("Provided settings %s", settings)
    cl.user_session.set("model", settings["model"])
    cl.user_session.set("stream", settings["stream"])
    cl.user_session.set("temperature", settings["temperature"])


@cl.on_message
async def message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})
    print(message_history)

    msg = cl.Message(content="")
    await msg.send()

    response = await ollmutils.ollama_client.chat(
        model=cl.user_session.get("model"),
        options=Options(temperature=cl.user_session.get("temperature")),
        messages=message_history,
        stream=cl.user_session.get("stream"),
    )

    if cl.user_session.get("stream"):
        async for part in response:
            if "message" in part and "content" in part["message"]:
                await msg.stream_token(part["message"]["content"])
    else:
        print(response)
        if "message" in response and "content" in response["message"]:
            msg.content = response["message"]["content"]
            await msg.send()

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
