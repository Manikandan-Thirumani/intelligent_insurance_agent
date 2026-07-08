# Intelligent Insurance Agent

This project is a starter scaffold for an intelligent insurance assistant.

## Structure

- src/intelligent_insurance_agent/agent.py: core assistant logic
- tests/test_agent.py: basic regression tests

## Run locally

Make sure Ollama is running locally and has a model available, for example:

```bash
ollama pull llama3.2:latest
```

Then run:

```bash
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m intelligent_insurance_agent.agent
```

You can override the default model or endpoint with:

```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.2:latest
```
