# Intelligent Insurance Agent

This project is a starter RAG-style insurance assistant with:

- a FastAPI service for chat, health, upload, and document listing
- a simple CLI RAG workflow for indexing documents and answering prompts
- sample insurance-related data and prompts

## Project structure

- src/intelligent_insurance_agent/Api: FastAPI endpoint modules
- src/intelligent_insurance_agent/Core: environment config and testing prompts
- src/intelligent_insurance_agent/Database: sample insurance data and seeding helpers
- src/intelligent_insurance_agent/Model: chat and document abstractions
- src/intelligent_insurance_agent/RAG: loader, splitter, embedding, vector store, retriever, and chain components
- src/intelligent_insurance_agent/main.py: RAG CLI implementation

## Setup

```bash
cd /home/labuser/project/intelligent_insurance_agent
PYTHONPATH=src python -m pip install -e .
```

## Run tests

```bash
PYTHONPATH=src python -m pytest
```

## Run the RAG CLI

```bash
PYTHONPATH=src python main.py --document /path/to/document.txt --prompt "What does the policy cover?"
```

Or run interactively:

```bash
PYTHONPATH=src python main.py
```

## Run the API

```bash
PYTHONPATH=src uvicorn intelligent_insurance_agent.api:app --host 127.0.0.1 --port 8000
```

Then visit:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/ for the chatbot frontend

