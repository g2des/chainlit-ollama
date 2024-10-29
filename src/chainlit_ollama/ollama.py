"""Ollama clients and connectors."""
from typing import List, LiteralString
import ollama as ol

ollama_client = ol.AsyncClient(host="http://host.docker.internal:11434")

async def get_models() -> List[LiteralString]:
    model_dict = await ollama_client.list()
    return [model["name"] for model in model_dict["models"]]