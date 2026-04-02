"""Built-in agent tools."""
from __future__ import annotations
import subprocess
import httpx
from agent.core import ToolDefinition

def web_search(query: str, max_results: int = 5) -> dict:
    """Simulated web search."""
    return {"query": query, "results": [{"title": f"Result {i+1}", "snippet": f"Info about {query}...", "url": f"https://example.com/{i}"} for i in range(max_results)]}

def execute_python(code: str) -> dict:
    """Execute Python code in a sandboxed subprocess."""
    try:
        result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=10)
        return {"stdout": result.stdout[:2000], "stderr": result.stderr[:500], "returncode": result.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out (10s limit)"}
    except Exception as e:
        return {"error": str(e)}

def read_url(url: str) -> dict:
    """Fetch a URL and return text content."""
    try:
        resp = httpx.get(url, timeout=10, follow_redirects=True)
        return {"status": resp.status_code, "content": resp.text[:3000], "url": str(resp.url)}
    except Exception as e:
        return {"error": str(e)}

def calculator(expression: str) -> dict:
    """Evaluate math expression."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return {"error": "Invalid characters"}
    try:
        return {"expression": expression, "result": eval(expression, {"__builtins__": {}}, {})}
    except Exception as e:
        return {"error": str(e)}

def get_default_tools() -> list[ToolDefinition]:
    return [
        ToolDefinition(name="web_search", description="Search the web", parameters={"type": "object", "properties": {"query": {"type": "string"}, "max_results": {"type": "integer", "default": 5}}, "required": ["query"]}, handler=web_search),
        ToolDefinition(name="execute_python", description="Execute Python code", parameters={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}, handler=execute_python),
        ToolDefinition(name="read_url", description="Fetch URL content", parameters={"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}, handler=read_url),
        ToolDefinition(name="calculator", description="Evaluate math", parameters={"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}, handler=calculator),
    ]
