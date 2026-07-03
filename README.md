# Automation Backend

Django backend for managing LLM models and agents, with a chat API powered by the OpenAI Python SDK.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py seed_llm_models
python manage.py createsuperuser
python manage.py runserver
```

Admin: http://localhost:8000/admin/

## Agent tools

Tools are defined in Django admin (**Agent Tools**) and written to `llm/tools/generated/`.
That folder is gitignored — generate files on each server after deploy.

```bash
python manage.py seed_example_tool   # optional demo: get_ticket_price
```

1. Create an **Agent Tool** in admin (name, description, parameters JSON, Python body)
2. Save — a `.py` file is generated automatically
3. Assign tools to an **LLM Agent** via the Tools field
4. Agents with no tools behave as normal chat

Example `python_code` body:

```python
destination_city = kwargs["destination_city"]
return f"Ticket to {destination_city} is $899"
```

## Models

- **LlmModel** — name, description, active
- **LlmAgent** — model (FK), name, role, context, tools, use_other_agent, base_url, api_key, active
- **AgentTool** — name, description, parameters, python_code (generates file on save)

## API

### List agents

`GET /api/agents/`

### Chat history (per user session)

`GET /api/chat/history/?agent_id=1&event_id=<uuid>`

### Stream chat

`POST /api/chat/` (Server-Sent Events)

```json
{
  "agent_id": 1,
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "prompt": "Tell me a fun fact"
}
```

Each SSE event includes `event_id` and `agent_id` so clients only process their own stream.

Event types: `start`, `chunk`, `done`, `error`

```json
{
  "agent": "My Agent",
  "model": "gpt-5-nano",
  "content": "..."
}
```

## Agent providers

**OpenAI (default)** — set `use_other_agent` to false and provide `api_key`.

**Ollama** — set `use_other_agent` to true:

- base_url: `http://localhost:11434/v1`
- api_key: `ollama`

**Gemini** — set `use_other_agent` to true:

- base_url: `https://generativelanguage.googleapis.com/v1beta/openai/`
- api_key: your Google API key
