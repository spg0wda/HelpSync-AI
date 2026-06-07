from fastapi import APIRouter
from pydantic import BaseModel

from agents.langgraph_supervisor import run_langgraph_workflow
from agents.memory_agent import get_recent_conversations
from agents.dashboard_agent import (
    get_dashboard_stats,
    get_all_tickets,
    get_all_escalations
)

router = APIRouter()


class ChatRequest(BaseModel):
    user_query: str


@router.post("/chat")
def chat(request: ChatRequest):
    result = run_langgraph_workflow(request.user_query)

    return {
        "current_stage": "Phase 9 - Dashboard APIs",
        **result
    }


@router.get("/history")
def history():
    conversations = get_recent_conversations(limit=10)

    return {
        "current_stage": "Phase 9 - Dashboard APIs",
        "total_returned": len(conversations),
        "conversations": conversations
    }


@router.get("/dashboard/stats")
def dashboard_stats():
    stats = get_dashboard_stats()

    return {
        "current_stage": "Phase 9 - Dashboard APIs",
        "dashboard": stats
    }


@router.get("/dashboard/tickets")
def dashboard_tickets():
    tickets = get_all_tickets()

    return {
        "current_stage": "Phase 9 - Dashboard APIs",
        "total_tickets": len(tickets),
        "tickets": tickets
    }


@router.get("/dashboard/escalations")
def dashboard_escalations():
    escalations = get_all_escalations()

    return {
        "current_stage": "Phase 9 - Dashboard APIs",
        "total_escalations": len(escalations),
        "escalations": escalations
    }