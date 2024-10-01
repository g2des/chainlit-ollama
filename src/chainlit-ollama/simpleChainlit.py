from typing import LiteralString, List
import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
import ollama as ol
from chainlit.logger import logger

ollama_client = ol.AsyncClient(host="http://host.docker.internal:11434")

async def get_models()-> List[LiteralString]:
    model_dict = await ollama_client.list()
    return [ model["name"] for model in model_dict["models"]]

@cl.on_chat_start
async def start_chat():
    models = await get_models()
    default_model = models[0]
    settings = await cl.ChatSettings(
        [
            Select(
                id="model",
                label="Ollama - Models",
                values=models,
                initial_index=0,
            ),
            Switch(id="stream", label="Stream Tokens", initial=True),
        ]
    ).send()
    await settings_update(settings)
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

@cl.on_settings_update
async def settings_update(settings):
    logger.info("Provided settings %s", settings)
    cl.user_session.set("model", settings['model'])
    cl.user_session.set("stream", settings['stream'])
    

@cl.on_message
async def message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    response = await ollama_client.chat(model=cl.user_session.get('model'), 
        messages=message_history, stream=cl.user_session.get('stream'), 
    )

    if cl.user_session.get('stream'):
        async for part in response:
            if 'message' in part and 'content' in part['message']:
                await msg.stream_token(part['message']['content'])
    else:
        print(response)
        if 'message' in response and 'content' in response['message']:
            msg.content = response["message"]["content"]
            await msg.send()


    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()