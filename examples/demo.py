"""
Demo: Agent with tool chaining — runs without API key using mock responses.
Run: python examples/demo.py
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

class MockAgent:
    """Simulates the agent loop with tool calls to show how it works."""
    
    def __init__(self):
        self.tools = {
            "search_web": lambda q: f"Found 3 results for '{q}': 1) Wikipedia article, 2) Blog post, 3) News article",
            "calculate": lambda expr: str(eval(expr)),
            "get_weather": lambda city: f"{city}: 72°F, sunny, humidity 45%",
            "create_task": lambda title: f"Task created: '{title}' (id: task_001)",
            "send_email": lambda to: f"Email drafted to {to} (not sent in demo mode)",
        }
        self.history = []
    
    def run(self, query: str):
        print(f"\n👤 User: {query}")
        self.history.append({"role": "user", "content": query})
        
        # Simulate agent reasoning + tool calls
        if "weather" in query.lower():
            self._call_tool("get_weather", "San Francisco")
            self._respond("Based on the weather data, San Francisco is 72°F and sunny today. Great day to be outside!")
        elif "calculate" in query.lower() or "%" in query or "tip" in query.lower():
            self._call_tool("calculate", "85.50 * 0.15")
            self._respond("A 15% tip on $85.50 would be $12.83, making the total $98.33.")
        elif "search" in query.lower() or "find" in query.lower():
            self._call_tool("search_web", query.replace("search for ", "").replace("find ", ""))
            self._respond("I found several relevant results. The Wikipedia article has the most comprehensive overview.")
        elif "task" in query.lower() or "remind" in query.lower():
            self._call_tool("create_task", "Review Q3 report")
            self._call_tool("send_email", "team@example.com")
            self._respond("Done! I created the task and drafted an email to your team about it.")
        else:
            self._respond(f"I understand you're asking about: {query}. Let me help with that.")
    
    def _call_tool(self, name, arg):
        result = self.tools[name](arg)
        print(f"   🔧 Tool: {name}({arg!r})")
        print(f"   📎 Result: {result}")
        self.history.append({"role": "tool", "name": name, "result": result})
    
    def _respond(self, text):
        print(f"🤖 Agent: {text}")
        self.history.append({"role": "assistant", "content": text})

def main():
    print("🤖 AI Agent Demo — Tool Chaining")
    print("=" * 50)
    print("Available tools: search_web, calculate, get_weather, create_task, send_email")
    
    agent = MockAgent()
    
    # Demo conversation showing tool chaining
    agent.run("What's the weather in San Francisco?")
    agent.run("Calculate a 15% tip on $85.50")
    agent.run("Search for recent developments in AI agents")
    agent.run("Create a task to review the Q3 report and email the team about it")
    
    print(f"\n📊 Session stats: {len(agent.history)} messages, {sum(1 for h in agent.history if h['role']=='tool')} tool calls")

if __name__ == "__main__":
    main()
