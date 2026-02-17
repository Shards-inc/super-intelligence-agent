import os
from typing import Any, Dict, List
from langchain.tools import Tool
from duckduckgo_search import DDGS

def web_search(query: str) -> str:
    """Perform a web search using DuckDuckGo."""
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query, max_results=5)]
        return "\n\n".join(results)

def python_executor(code: str) -> str:
    """Execute Python code in a restricted environment (simulated)."""
    # In a real production environment, use a proper sandbox like E2B or Docker
    try:
        local_vars = {}
        exec(code, {"__builtins__": __builtins__}, local_vars)
        return str(local_vars.get('result', 'Code executed successfully.'))
    except Exception as e:
        return f"Error: {str(e)}"

# Define LangChain tools
tools = [
    Tool(
        name="WebSearch",
        func=web_search,
        description="Useful for searching the internet for current information."
    ),
    Tool(
        name="PythonExecutor",
        func=python_executor,
        description="Useful for executing Python code to perform calculations or data processing. Set the final output to a variable named 'result'."
    )
]
