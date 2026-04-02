"""AI Agent with ReAct reasoning loop, tool chaining, and memory."""
from __future__ import annotations
import json, logging
from dataclasses import dataclass, field
from typing import Any, Callable
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)
client = AsyncOpenAI()

@dataclass
class AgentConfig:
    model: str = "gpt-4o"
    max_iterations: int = 10
    temperature: float = 0.3
    system_prompt: str = "You are a helpful AI agent. Use tools when needed. Think step by step."

@dataclass
class AgentMemory:
    short_term: list[dict] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.short_term.append({"role": role, "content": content})
        if len(self.short_term) > 30: self.short_term = self.short_term[-30:]

    def add_fact(self, fact: str) -> None:
        if fact not in self.facts: self.facts.append(fact)

    def get_context(self) -> str:
        if not self.facts: return ""
        return "Known facts:\n" + "\n".join(f"- {f}" for f in self.facts[-10:])

@dataclass
class ToolResult:
    tool_name: str
    arguments: dict
    result: Any
    success: bool = True

@dataclass
class AgentResponse:
    answer: str
    tool_calls: list[ToolResult]
    iterations: int
    reasoning: list[str]

class Agent:
    def __init__(self, config: AgentConfig | None = None):
        self.config = config or AgentConfig()
        self.memory = AgentMemory()
        self._tools: dict[str, dict] = {}
        self._handlers: dict[str, Callable] = {}

    def register_tool(self, name: str, description: str, parameters: dict, handler: Callable) -> None:
        self._tools[name] = {"type": "function", "function": {"name": name, "description": description, "parameters": parameters}}
        self._handlers[name] = handler

    async def run(self, query: str) -> AgentResponse:
        self.memory.add_message("user", query)
        tool_calls_made: list[ToolResult] = []
        reasoning: list[str] = []
        messages = [
            {"role": "system", "content": f"{self.config.system_prompt}\n\n{self.memory.get_context()}"},
            *self.memory.short_term,
        ]
        tools = list(self._tools.values()) if self._tools else None

        for iteration in range(self.config.max_iterations):
            response = await client.chat.completions.create(model=self.config.model, messages=messages, tools=tools, temperature=self.config.temperature)
            msg = response.choices[0].message

            if not msg.tool_calls:
                answer = msg.content or ""
                self.memory.add_message("assistant", answer)
                return AgentResponse(answer=answer, tool_calls=tool_calls_made, iterations=iteration + 1, reasoning=reasoning)

            messages.append(msg.model_dump())
            for tc in msg.tool_calls:
                fn_name = tc.function.name
                fn_args = json.loads(tc.function.arguments)
                reasoning.append(f"Calling {fn_name}({json.dumps(fn_args)[:100]})")
                handler = self._handlers.get(fn_name)
                if handler:
                    try:
                        result = handler(**fn_args)
                        if hasattr(result, "__await__"): result = await result
                        tool_calls_made.append(ToolResult(tool_name=fn_name, arguments=fn_args, result=result))
                    except Exception as e:
                        result = {"error": str(e)}
                        tool_calls_made.append(ToolResult(tool_name=fn_name, arguments=fn_args, result=result, success=False))
                else:
                    result = {"error": f"Unknown tool: {fn_name}"}
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result) if not isinstance(result, str) else result})

        return AgentResponse(answer="Max iterations reached", tool_calls=tool_calls_made, iterations=self.config.max_iterations, reasoning=reasoning)
