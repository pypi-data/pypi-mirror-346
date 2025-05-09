# ab_sdk/agent.py

import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests

load_dotenv()

# ========== Gemini Setup ==========
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No GEMINI_API_KEY found. Set it in .env.")
genai.configure(api_key=api_key)

# ========== Tool Interface ==========
class Tool:
    def __init__(self, name: str, description: str, func):
        self.name = name
        self.description = description
        self.func = func

    def run(self, query: str):
        return self.func(query)

# ========== Built-in Tools ==========

# Weather Tool (Tavily)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def get_weather(query: str):
    if not TAVILY_API_KEY:
        return "Missing Tavily API key."

    try:
        response = requests.get(
            "https://api.tavily.com/search",
            params={"api_key": TAVILY_API_KEY, "query": f"weather in {query}", "search_depth": "basic"},
        )
        data = response.json()
        return data.get("results", ["No result found"])[0]
    except Exception as e:
        return f"Error fetching weather: {e}"

# Calculator Tool
def calculate(query: str):
    try:
        return f"Result: {eval(query)}"
    except Exception as e:
        return f"Error: {e}"

class Agent:
    def __init__(
        self,
        name: str,
        instructions: str,
        model_name: str = "gemini-1.5-flash",
        temperature: float = 0.7,
        model: genai.GenerativeModel = None,
        handoffs: list = None,
        tools: list = None,
    ):
        self.name = name
        self.instructions = instructions
        self.handoffs = {agent.name.lower(): agent for agent in (handoffs or [])}
        self.tools = {tool.name.lower(): tool for tool in (tools or [])}

        self.model = model or genai.GenerativeModel(
            model_name=model_name,
            system_instruction=instructions,
            generation_config=genai.GenerationConfig(temperature=temperature),
        )

    def add_tool(self, tool: Tool):
        self.tools[tool.name.lower()] = tool

    def add_handoff(self, agent):
        self.handoffs[agent.name.lower()] = agent

    def tool_execute(self, tool_name: str, query: str):
        tool = self.tools.get(tool_name.lower())
        if tool:
            return tool.run(query)
        return f"Tool '{tool_name}' not found."

    def to_tool(self, name: str = None, description: str = None):
        """
        Converts this Agent into a Tool that can be used by other agents.
        """
        return Tool(
            name=name or self.name,
            description=description or f"Tool interface for agent: {self.name}",
            func=self.run
        )

    def run(self, prompt: str = "") -> str:
        if prompt.lower().startswith("use tool:"):
            try:
                _, tool_name, *query_parts = prompt.split(":")
                query = ":".join(query_parts).strip()
                return self.tool_execute(tool_name.strip(), query)
            except:
                return "Invalid tool usage. Format: use tool: tool_name: your query"

        response = self.model.generate_content(
            f"{prompt}\n\nIf another agent is better, respond with 'HANDOFF: <agent_name>'. Otherwise answer normally."
        )
        text = response.text.strip()

        if text.startswith("HANDOFF:"):
            target_name = text.replace("HANDOFF:", "").strip().lower()
            target_agent = self.handoffs.get(target_name)
            if target_agent:
                return f"[{self.name} → {target_agent.name}]\n" + target_agent.run(prompt)
            else:
                return f"[{self.name}] No agent named '{target_name}' for handoff."

        return text
