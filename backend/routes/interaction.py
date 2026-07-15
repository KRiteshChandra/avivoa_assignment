from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from ai.graph import build_graph, SYSTEM_PROMPT
from ai.tools import log_interaction, get_history

router = APIRouter(prefix="/interaction", tags=["interaction"])

graph = build_graph()


class ChatRequest(BaseModel):
    input_text: str


class LogRequest(BaseModel):
    hcp_name: str
    topic: str
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    followup: Optional[str] = None


@router.post("/chat")
def chat(request: ChatRequest):
    """
    Conversational entry point. Goes through the full LangGraph agent,
    which decides which of the 5 tools to call based on the message.
    """
    initial_state = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.input_text}
        ],
        "output": {}
    }
    result = graph.invoke(initial_state)
    return {
        "status": "success",
        "response": result.get("output")
    }


@router.post("/log")
def log_structured(request: LogRequest):
    """
    Structured-form entry point. Calls the log_interaction tool directly
    (bypassing LLM tool-selection, since the fields are already structured).
    Reuses the same underlying tool function used by the chat agent.
    """
    result = log_interaction(request.dict())
    return {"status": "success", "response": result}


@router.get("/history")
def history(hcp_name: Optional[str] = None, limit: int = 20):
    """Direct DB read for populating the frontend history list."""
    result = get_history({"hcp_name": hcp_name, "limit": limit})
    return {"status": "success", "response": result["result"]}


@router.get("/")
def test():
    return {"message": "Interaction route working"}
