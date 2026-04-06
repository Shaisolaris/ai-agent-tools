import os
# Demo mode: runs with sample data when no API keys configured
DEMO_MODE = os.getenv('DEMO_MODE', 'false').lower() == 'true' or not os.getenv('DATABASE_URL')
"""FastAPI for AI Agent."""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from agent.core import Agent, AgentConfig
from tools.web import web_search, web_fetch, SEARCH_DEFINITION, FETCH_DEFINITION
from tools.code import execute_code, CODE_DEFINITION
from tools.memory import save_memory, recall_memory, SAVE_DEFINITION, RECALL_DEFINITION

app = FastAPI(title="AI Agent API", version="1.0.0")

def create_agent() -> Agent:
    a = Agent(AgentConfig())
    a.register_tool("web_search", "Search the web", SEARCH_DEFINITION, web_search)
    a.register_tool("web_fetch", "Fetch a web page", FETCH_DEFINITION, web_fetch)
    a.register_tool("execute_code", "Execute Python code", CODE_DEFINITION, execute_code)
    a.register_tool("save_memory", "Save information for later", SAVE_DEFINITION, save_memory)
    a.register_tool("recall_memory", "Recall saved information", RECALL_DEFINITION, recall_memory)
    return a

_agent = create_agent()

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    max_iterations: int = 10

@app.get("/health")
def health(): return {"status": "healthy", "tools": list(_agent._tools.keys())}

@app.post("/agent/run")
async def run_agent(req: QueryRequest):
    _agent.config.max_iterations = req.max_iterations
    result = await _agent.run(req.query)
    return {"answer": result.answer, "tool_calls": [{"tool": tc.tool_name, "args": tc.arguments, "result": tc.result, "success": tc.success} for tc in result.tool_calls], "iterations": result.iterations, "reasoning": result.reasoning}
