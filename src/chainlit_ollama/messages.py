"""This module deals with messages from users."""
import chainlit as cl
from ollama import Options

from chainlit_ollama import ollama as ollmutils

async def on_messages(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

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