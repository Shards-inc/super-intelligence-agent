from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
from core.llm_manager import LLMManager
from agents.crew_agent import CrewAIAgentWrapper
from agents.langgraph_orchestrator import LangGraphOrchestrator
from loguru import logger

app = FastAPI(title="Super-Intelligence Agent API")
llm_manager = LLMManager()

class QueryRequest(BaseModel):
    query: str
    agent_type: str = "crewai" # crewai, langgraph, autogen
    model: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "online", "message": "Super-Intelligence Agent API is running."}

@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        if request.agent_type == "crewai":
            agent = CrewAIAgentWrapper(
                name="GeneralAssistant",
                role="Helpful Assistant",
                goal="Provide accurate and helpful information.",
                backstory="An advanced AI agent capable of multi-step reasoning.",
                model_name=request.model or "gpt-4o"
            )
            response = await agent.run(request.query)
            return response
        elif request.agent_type == "langgraph":
            # Simplified LangGraph call
            orchestrator = LangGraphOrchestrator(model=llm_manager)
            response = await orchestrator.run(request.query)
            return response
        else:
            raise HTTPException(status_code=400, detail="Unsupported agent type.")
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
