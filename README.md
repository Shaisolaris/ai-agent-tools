# ai-agent-tools

AI agent with ReAct reasoning loop, 5 tools (web search, web fetch, code execution, save memory, recall memory), automatic tool chaining, and conversation memory. Uses OpenAI function calling for tool selection and FastAPI for serving.

## Tools
- **web_search** — Search the web for information
- **web_fetch** — Fetch and read web page content
- **execute_code** — Sandboxed Python code execution
- **save_memory** — Persist key-value pairs across turns
- **recall_memory** — Retrieve saved information

## API
| Method | Endpoint | Description |
|---|---|---|
| POST | `/agent/run` | Run agent with query (auto-selects tools) |
| GET | `/health` | Status + registered tools |

## Architecture
```
agent/core.py    — Agent class with ReAct loop, memory, tool registry
tools/web.py     — Web search + fetch
tools/code.py    — Sandboxed Python execution
tools/memory.py  — Key-value memory store
api/app.py       — FastAPI endpoint
```

## Setup
```bash
git clone https://github.com/Shaisolaris/ai-agent-tools.git
cd ai-agent-tools && pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python main.py
```

## License
MIT
