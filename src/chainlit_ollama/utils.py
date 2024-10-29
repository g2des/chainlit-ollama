"""Chainlit Utils."""
import chainlit as cl

from chainlit_ollama import utils as cl_utils
from chainlit.input_widget import Select, Switch, Slider
from chainlit.logger import logger

from chainlit_ollama import ollama as ollmutils
from chainlit_ollama import settings as clsettings
chat_profiles = [
        cl.ChatProfile(
            name="Phi3.5",
            icon="https://picsum.photos/250",
            markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
            starters=[
                cl.Starter(
                    label="Morning routine ideation",
                    message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
                    icon="/public/idea.png",
                ),
                cl.Starter(
                    label="Explain superconductors",
                    message="Explain superconductors like I'm five years old.",
                    icon="/public/learn.svg",
                ),
            ],
        ),
        cl.ChatProfile(
            name="Llama3.2",
            icon="https://picsum.photos/251",
            markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
            starters=[
                cl.Starter(
                    label="Morning routine ideation",
                    message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
                    icon="/public/idea.png",
                ),
                cl.Starter(
                    label="Explain superconductors",
                    message="Explain superconductors like I'm five years old.",
                    icon="/public/learn.svg",
                ),
            ],
        )
    ]

async def start_chat():
    models = await ollmutils.get_models()
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
            Slider(
                id="temperature",
                label="Ollama - Temperature",
                initial=0.6,
                min=0,
                max=1,
                step=0.1,
            ),
        ]
    ).send()
    print(settings)
    await clsettings.settings(settings)
    cl.user_session.set(
        "message_history",
        [
            {
                "role": "system",
                "content": "You are a helpful assistant. Your answsers are always formatted properly.",
            }
        ],
    )