"""Settings module for chainlit."""

import chainlit as cl
import chainlit.logger as logger

async def settings(settings):
    logger.info("Provided settings %s", settings)
    cl.user_session.set("model", settings["model"])
    cl.user_session.set("stream", settings["stream"])
    cl.user_session.set("temperature", settings["temperature"])
