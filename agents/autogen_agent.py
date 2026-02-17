import autogen
from typing import Any, Dict, List, Optional
from core.base_agent import BaseAgent, AgentResponse

class AutoGenAgentWrapper(BaseAgent):
    def __init__(self, name: str, role: str, model_name: str, system_message: str):
        super().__init__(name, role, model_name)
        self.config_list = [{"model": model_name, "api_key": "dummy"}] # API key handled by env
        self.agent = autogen.AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config={"config_list": self.config_list}
        )
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "coding", "use_docker": False},
        )

    async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        # Note: AutoGen's initiate_chat is synchronous, in a real app we'd wrap it
        self.user_proxy.initiate_chat(self.agent, message=task)
        last_msg = self.user_proxy.last_message()["content"]
        return AgentResponse(content=last_msg, metadata={"agent": self.name})
