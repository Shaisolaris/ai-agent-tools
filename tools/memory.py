"""Memory management tools."""
SAVE_DEFINITION = {"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "string"}}, "required": ["key", "value"]}
RECALL_DEFINITION = {"type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]}

_store: dict[str, str] = {}

def save_memory(key: str, value: str) -> dict:
    _store[key] = value
    return {"saved": True, "key": key}

def recall_memory(key: str) -> dict:
    return {"key": key, "value": _store.get(key), "found": key in _store}
