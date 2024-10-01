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
- Run Chainlit App
```bash
poetry run chainlit run src/chainlit-ollama/simpleChainlit.py
```