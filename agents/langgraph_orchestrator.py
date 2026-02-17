from typing import Annotated, TypedDict, Union, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage
from core.base_agent import AgentResponse

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]
    next_step: str

class LangGraphOrchestrator:
    def __init__(self, model):
        self.model = model
        self.workflow = StateGraph(AgentState)
        self._setup_graph()

    def _setup_graph(self):
        self.workflow.add_node("reasoning", self.reasoning_node)
        self.workflow.add_node("action", self.action_node)
        
        self.workflow.set_entry_point("reasoning")
        self.workflow.add_conditional_edges(
            "reasoning",
            self.should_continue,
            {
                "continue": "action",
                "end": END
            }
        )
        self.workflow.add_edge("action", "reasoning")
        self.app = self.workflow.compile()

    def reasoning_node(self, state: AgentState):
        messages = state['messages']
        response = self.model.invoke(messages)
        return {"messages": [response]}

    def action_node(self, state: AgentState):
        # Placeholder for tool execution logic
        return {"messages": [HumanMessage(content="Action executed.")]}

    def should_continue(self, state: AgentState):
        last_message = state['messages'][-1]
        if "FINAL ANSWER" in last_message.content:
            return "end"
        return "continue"

    async def run(self, query: str) -> AgentResponse:
        inputs = {"messages": [HumanMessage(content=query)]}
        result = await self.app.ainvoke(inputs)
        return AgentResponse(content=result['messages'][-1].content, metadata={"history": result['messages']})
