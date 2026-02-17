from pydantic_ai import Agent
from typing import Any, Dict, Optional
from core.base_agent import BaseAgent, AgentResponse

class PydanticAIAgentWrapper(BaseAgent):
    def __init__(self, name: str, role: str, model_name: str, system_prompt: str):
        super().__init__(name, role, model_name)
        self.agent = Agent(
            model_name,
            system_prompt=system_prompt,
        )

    async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        result = await self.agent.run(task)
        return AgentResponse(content=result.data, metadata={"usage": result.usage()})
