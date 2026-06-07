from fastapi import APIRouter
from pydantic import BaseModel

from agents.langgraph_supervisor import run_langgraph_workflow

router = APIRouter()


class ChatRequest(BaseModel):
    user_query: str


@router.post("/chat")
def chat(request: ChatRequest):
    result = run_langgraph_workflow(request.user_query)

    return {
        "current_stage": "Phase 7 - LangGraph Supervisor Workflow",
        **result
    }