# Chainlit and Ollama

## Setup

- Install Ollama
- Pull some models
```bash
ollama pull llama3.2
ollama pull phi3.5
```
- Start Ollama server from your command line
```bash
ollama serve
```
- Open the repo in devcontainer and do poetry install
```bash
poetry install
```

## Simple Chainlit Ollama App

This is a simple app, that connects chainlit with Ollama. It has following features:
- It lists all the models that are already available on the local system
- It allows you to select between the listed models
- It allows you to set temperature
- Run Simple Chainlit App
```bash
poetry run chainlit run chainlit.py
```