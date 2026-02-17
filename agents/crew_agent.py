from crewai import Agent, Task, Crew, Process
from typing import List, Any, Dict, Optional
from core.base_agent import BaseAgent, AgentResponse

class CrewAIAgentWrapper(BaseAgent):
    def __init__(self, name: str, role: str, goal: str, backstory: str, model_name: str, tools: List[Any] = []):
        super().__init__(name, role, model_name)
        self.goal = goal
        self.backstory = backstory
        self.tools = tools
        self.agent = Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=self.tools,
            llm=self.model_name,
            verbose=True,
            allow_delegation=True
        )

    async def run(self, task_description: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="A comprehensive response based on the task description."
        )
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential
        )
        result = crew.kickoff()
        return AgentResponse(content=str(result), metadata={"crew_result": result})
