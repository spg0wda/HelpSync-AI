from fastapi import APIRouter
from pydantic import BaseModel

from agents.langgraph_supervisor import run_langgraph_workflow
from agents.memory_agent import get_recent_conversations

router = APIRouter()


class ChatRequest(BaseModel):
    user_query: str


@router.post("/chat")
def chat(request: ChatRequest):
    result = run_langgraph_workflow(request.user_query)

    return {
        "current_stage": "Phase 8 - Conversation Memory",
        **result
    }


@router.get("/history")
def history():
    conversations = get_recent_conversations(limit=10)

    return {
        "current_stage": "Phase 8 - Conversation Memory",
        "total_returned": len(conversations),
        "conversations": conversations
    }