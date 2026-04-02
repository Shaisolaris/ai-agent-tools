"""Web search and fetch tools."""
import httpx

SEARCH_DEFINITION = {"type": "object", "properties": {"query": {"type": "string"}, "num_results": {"type": "integer", "default": 3}}, "required": ["query"]}
FETCH_DEFINITION = {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}

def web_search(query: str, num_results: int = 3) -> dict:
    return {"query": query, "results": [{"title": f"Result {i+1}: {query}", "url": f"https://example.com/r/{i}", "snippet": f"Information about {query}..."} for i in range(num_results)]}

async def web_fetch(url: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(url)
            return {"url": url, "status": r.status_code, "content": r.text[:2000]}
    except Exception as e:
        return {"error": str(e)}
