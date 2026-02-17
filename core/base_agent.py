from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class AgentResponse(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, model_name: str):
        self.name = name
        self.role = role
        self.model_name = model_name

    @abstractmethod
    async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        pass
